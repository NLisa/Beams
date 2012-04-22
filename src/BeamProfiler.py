#coding: utf8
import numpy as N
from traits.api import (HasTraits, Bool, Int, Float, Array, Tuple, Instance,
    Property, on_trait_change)
from traitsui.api import View, VGroup, Item
from enable.api import ColorTrait
from CameraImage import CameraImage

class BeamProfiler(HasTraits):

    active = Bool(False)
    frame = Array(dtype=float)
    screen = Instance(CameraImage)
    background_percentile = Float(15)
    num_crops = Int(1)
    crop_radius = Float(1.5)  # in beam diameters

    centroid = Tuple(Float(0), Float(0))
    width = Float(1)
    height = Float(1)
    angle = Float(0)
    num_points = Int(40)
    color = ColorTrait('white')

    view = View(
        VGroup(
            Item('active'),
            Item('background_percentile'),
            Item('num_crops', label='Crop # times'),
            Item('crop_radius'),
            label='Beam Profiler',
            show_border=True))

    def __init__(self, **traits):
        HasTraits.__init__(self, **traits)
        self.screen.data_store['centroid_x'] = N.array([])
        self.screen.data_store['centroid_y'] = N.array([])
        self.screen.data_store['ellipse_x'] = N.array([])
        self.screen.data_store['ellipse_y'] = N.array([])
        renderers = self.screen.plot.plot(('centroid_x', 'centroid_y'),
            type='scatter',
            marker_size=2.0,
            color=self.color,
            marker='circle')
        self._centroid_patch = renderers[0]
        self._centroid_patch.visible = self.active
        renderers = self.screen.plot.plot(('ellipse_x', 'ellipse_y'),
            type='line',
            color=self.color)
        self._ellipse_patch = renderers[0]
        self._ellipse_patch.visible = self.active

    def _centroid_changed(self):
        self.screen.data_store['centroid_x'] = N.array([self.centroid[0]])
        self.screen.data_store['centroid_y'] = N.array([self.centroid[1]])

    @on_trait_change('centroid,width,height,angle')
    def _redraw_ellipse(self):
        # Draw an N-point ellipse at the 1/e radius of the Gaussian fit
        # Using a parametric equation in t
        t = N.linspace(0, 2 * N.pi, self.num_points)
        angle = N.radians(self.angle)
        r_a = self.width / 2.0
        r_b = self.height / 2.0
        x = (self.centroid[0] + r_a * N.cos(t) * N.cos(angle)
            - r_b * N.sin(t) * N.sin(angle))
        y = (self.centroid[1] + r_a * N.cos(t) * N.sin(angle)
            - r_b * N.sin(t) * N.cos(angle))
        self.screen.data_store['ellipse_x'] = x
        self.screen.data_store['ellipse_y'] = y

    def _frame_changed(self, frame):
        if not self.active:
            return

        bw = (len(frame.shape) == 2)
        if not bw:
            # Use standard NTSC conversion formula
            frame = N.array(
                0.2989 * frame[..., 0] 
                + 0.5870 * frame[..., 1]
                + 0.1140 * frame[..., 2])

        # Calibrate the background
        background = N.percentile(frame, self.background_percentile)
        frame -= background
        #N.clip(frame, 0.0, frame.max(), out=frame)

        m00, m10, m01, m20, m02, m11 = _calculate_moments(frame)

        bc, lc = 0, 0
        for count in range(self.num_crops):
            include_radius, dlc, dbc, drc, dtc, frame = _crop(frame,
                self.crop_radius, m00, m10, m01, m20, m02, m11)
            lc += dlc
            bc += dbc

            # Recalibrate the background and recalculate the moments
            new_bkg = N.percentile(frame, self.background_percentile)
            frame -= new_bkg
            background += new_bkg
            #N.clip(frame, 0.0, frame.max(), out=frame)

            m00, m10, m01, m20, m02, m11 = _calculate_moments(frame)

        m10 += lc
        m01 += bc

        # Calculate Gaussian boundary
        q = N.sqrt((m20 - m02) ** 2 + 4 * m11 ** 2)
        major_axis = 2 ** 1.5 * N.sqrt(m20 + m02 + q)
        minor_axis = 2 ** 1.5 * N.sqrt(m20 + m02 - q)
        rotation = N.degrees(0.5 * N.arctan2(2 * m11, m20 - m02))
        ellipticity = minor_axis / major_axis

        self.screen.hud('profiler',
            'Centroid: {:.1f}, {:.1f}\n'.format(m10, m01)
            + 'Major axis: {:.1f}\n'.format(major_axis)
            + 'Minor axis: {:.1f}\n'.format(minor_axis)
            + u'Rotation: {:.1f}°\n'.format(rotation)
            + 'Ellipticity: {:.3f}\n'.format(ellipticity)
            + 'Baseline: {:.1f}\n'.format(background)
            + 'Inclusion radius: {:.1f}'.format(include_radius))
        self.centroid = (m10, m01)
        self.width = minor_axis
        self.height = major_axis
        self.angle = rotation

    def _active_changed(self, value):
        if not value:
            self.screen.hud('profiler', None)
        self._centroid_patch.visible = value
        self._ellipse_patch.visible = value

def _calculate_moments(frame):
    """Calculate the moments"""
    # From Bullseye
    y, x = N.mgrid[:frame.shape[0], :frame.shape[1]]
    m00 = frame.sum() or 1.0
    m10 = (frame * x).sum() / m00
    m01 = (frame * y).sum() / m00
    dx, dy = x - m10, y - m01
    m20 = (frame * dx ** 2).sum() / m00
    m02 = (frame * dy ** 2).sum() / m00
    m11 = (frame * dx * dy).sum() / m00
    return m00, m10, m01, m20, m02, m11

def _crop(frame, crop_radius, m00, m10, m01, m20, m02, m11):
    """crop based on 3 sigma region"""
    w20 = crop_radius * 4 * N.sqrt(m20)
    w02 = crop_radius * 4 * N.sqrt(m02)
    include_radius = N.sqrt((w20 ** 2 + w02 ** 2) / 2)
    w02 = max(w02, 4)
    w20 = max(w20, 4)
    lc = int(max(0, m10 - w20))
    bc = int(max(0, m01 - w02))
    tc = int(min(frame.shape[0], m01 + w02))
    rc = int(min(frame.shape[1], m10 + w20))
    frame = frame[bc:tc, lc:rc]
    return include_radius, lc, bc, rc, tc, frame
