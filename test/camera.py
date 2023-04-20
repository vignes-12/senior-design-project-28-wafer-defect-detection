import os
import threading
import struct
import time

from pixelink import PixeLINK
from pixelink import PxLapi
from pixelink import PxLerror


def save_image(path, data):

    if os.path.exists(path):
        os.remove(path)

    name = path.lower()
    if name.endswith('.bmp'):
        save_as_bmp(path, data)

    elif name.endswith('.fits') or name.endswith('.fit'):
        save_as_fits(path, data)


def save_as_bmp(path, data):

    (h, w) = data.shape
    raw_bytes = data.tostring()
    info = {'width': w, 'height': h, 'colordepth': 8}

    # Here is a minimal dictionary with header values.
    # Of importance is the offset, headerlength, width,
    # height and colordepth.
    # Edit the width and height to your liking.
    # These header values are described in the bmp format spec.
    # You can find it on the internet. This is for a Windows
    # Version 3 DIB header.

    header_entries = (
        ('<B', 66, 'mn1'),
        ('<B', 77, 'mn2'),
        ('<L', 0, 'filesize'),
        ('<H', 0, 'undef1'),
        ('<H', 0, 'undef2'),
        ('<L', 54, 'offset'),
        ('<L', 40, 'headerlength'),
        ('<L', 0, 'width'),
        ('<L', 0, 'height'),
        ('<H', 0, 'colorplanes'),
        ('<H', 24, 'colordepth'),
        ('<L', 0, 'compression'),
        ('<L', 0, 'imagesize'),
        ('<L', 0, 'res_hor'),
        ('<L', 0, 'res_vert'),
        ('<L', 0, 'palette'),
        ('<L', 0, 'importantcolors'),
    )
    header = b''
    for entry in header_entries:
        frmt, val, key = entry
        if key in info:
            val = info[key]
        header += struct.pack(frmt, val)

    with open(path, 'wb') as outfile:
        outfile.write(header + raw_bytes)


def save_as_fits(fname, data, header=None, dtype=None):

    from astropy.io import fits as pyfits

    if dtype is not None:
        data = data.astype(dtype)
    fits = pyfits.PrimaryHDU(data)

    if header:
        for entry in header:
            try:
                fits.header.update(entry.key, entry.value, entry.desc)
            except ValueError as e:
                s = 'Failed to write fits header entry: '
                s += entry.key + '=' + str(entry.value) + ';' + str(e)
                print(s)

    fits.writeto(fname)


def test_camera_api():
    print('Running tests on the Camera API...')
    api = PxLapi()
    h_camera = None
    try:
        serial_nums = api.GetNumberCameras()
        print(serial_nums)

        h_camera = api.Initialize()

        print('pixel format', api.GetFeature(h_camera, PxLapi.FEATURE_PIXEL_FORMAT))
        api.SetFeature(h_camera, PxLapi.FEATURE_PIXEL_FORMAT, PxLapi.PIXEL_FORMAT_MONO16)
        print('pixel format', api.GetFeature(h_camera, PxLapi.FEATURE_PIXEL_FORMAT))

        # test integration time setting
        print('shutter', api.GetFeature(h_camera, PxLapi.FEATURE_SHUTTER))
        api.SetFeature(h_camera, PxLapi.FEATURE_SHUTTER, 0.1)
        print('shutter', api.GetFeature(h_camera, PxLapi.FEATURE_SHUTTER))
        report = api.GetErrorReport(h_camera)
        print('report', str(report))

        # test roi functionality
        roi = api.GetFeature(h_camera, PxLapi.FEATURE_ROI, 4)
        w = roi[2]
        h = roi[3]
        print('roi', api.GetFeature(h_camera, PxLapi.FEATURE_ROI, 4))
        try:
            api.SetFeature(h_camera, PxLapi.FEATURE_ROI, [0, 0, 1000, 1000])
        except PxLerror as ex:
            print(str(ex))
        print('roi', api.GetFeature(h_camera, PxLapi.FEATURE_ROI, 4))

        # test frame grabbing
        api.SetStreamState(h_camera, PxLapi.START_STREAM)
        try:
            for i in range(1):
                data = api.GetNextFrame(h_camera, w, h)
                print('grabbed frame #%02d' % i, data)
                report = api.GetErrorReport(h_camera)
                print('report', str(report))
        except PxLerror as ex:
            print(ex)
        api.SetStreamState(h_camera, PxLapi.STOP_STREAM)

    except PxLerror as ex:
        print(str(ex))

    finally:
        api.Uninitialize(h_camera)


def test_camera_class():
    print('Running tests on the Camera class...')
    cam = PixeLINK()
    shutter0 = cam.shutter
    print('shutter0', shutter0)
    roi0 = cam.roi
    print('roi0', roi0)

    cam.shutter = 1.5
    print('shutter', cam.shutter)

    # this will fail because the camera is streaming. Catch the error.
    try:
        cam.roi = [0, 0, 1000, 1000]
    except PxLerror as ex:
        print(str(ex))

    # stop the streaming and try to set to ROI again
    if cam.streaming:
        cam.streaming = False
        print('streaming', cam.streaming)

    # now the setting of the ROI will be set without errors.
    try:
        cam.roi = [0, 0, 1000, 1000]
        print('roi', cam.roi)
    except PxLerror as ex:
        print(str(ex))

    # test frame grabbing
    cam.streaming = True
    data = cam.grab()
    # print('data.shape', data.shape)
    cam.streaming = False

    # reset features to original values
    cam.roi = roi0
    cam.shutter = shutter0
    cam.close()

    save_image('test.bmp', data)


def grab_continuous(cam):
    frame_num = 0
    while cam.is_open():
        time_0 = time.time()
        frame_num += 1
        try:
            data = cam.grab()
        except PxLerror as exc:
            print('ERROR: grab_continuous:', str(exc))
            continue
        t_dif = time.time() - time_0
        if data is not None:
            print('#: %d, %0.3f sec, shape: %s, mean: %0.3f, std: %0.3f'
                  % (frame_num, t_dif, repr(data.shape), data.mean(), data.std()))
        time.sleep(0.001)


def test_thread_safe():
    cam = PixeLINK()
    # cam.streaming = False
    cam.shutter = 0.001
    data = cam.grab()
    # cam.binning = [2, 0]
    cam.roi = [0, 0, 1000, 1000]  # 0,0,2208,3000
    # cam.roi = [0, 0, 2208, 3000]  # 0,0,2208,3000

    th = threading.Thread(target=grab_continuous, args=[cam])
    th.start()
    time_0 = time.time()
    # cam.streaming = False
    t_dif = 0.0

    while t_dif < 5.0:
        cam.shutter += 0.0001
        cam.brightness += 0.001
        cam.gain += 0.001

        t_dif = time.time() - time_0
        print('ffcSupported:', cam.ffc_supported)
        print('ffcEnabled:', cam.ffc_enabled)
        print('ffcType:', cam.ffc_type)
        print('frameRate:', cam.frame_rate)
        print('sensorTemperature:', cam.sensor_temperature)
        print('gain:', cam.gain)
        print('shutter:', cam.shutter)
        print('pixelAddressing:', cam.pixel_addressing)
        print('pixelFormat:', cam.pixelFormat)
        print('memoryChannel:', cam.memory_channel)
        print('rotate:', cam.rotate)
        print('maxPixelSize:', cam.maxPixelSize)

        if cam.property_supported('WhiteShading'):
            print('whiteShading:', cam.white_shading)
        if cam.property_supported('Gamma'):
            print('gamma:', cam.gamma)
        if cam.property_supported('Saturation'):
            print('saturation:', cam.saturation)
        if cam.property_supported('Hue'):
            print('hue:', cam.hue)
        if cam.property_supported('ColorTemp'):
            print('colorTemp:', cam.color_temp)
        if cam.property_supported('Sharpness'):
            print('sharpness:', cam.sharpness)
        if cam.property_supported('Brightness'):
            print('brightness:', cam.brightness)
        if cam.property_supported('Flip'):
            print('flip:', cam.flip)
        if cam.property_supported('BodyTemperature'):
            print('bodyTemperature:', cam.body_temperature)
        if cam.property_supported('SharpnessScore'):
            print('sharpnessScore:', cam.sharpness_score)

        time.sleep(0.001)
    cam.close()


def run_tests():
    # test_camera_api()
    test_camera_class()
    # test_thread_safe()


if __name__ == '__main__':
    run_tests()
