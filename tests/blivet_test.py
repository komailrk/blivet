import test_compat  # pylint: disable=unused-import

from six.moves.mock import PropertyMock, patch  # pylint: disable=no-name-in-module,import-error
import unittest
from pykickstart.version import returnClassForVersion
from blivet import Blivet
from blivet.devices import PartitionDevice
from blivet import formats
from blivet.size import Size


class BlivetTestCase(unittest.TestCase):
    '''
    Define tests for the Blivet class
    '''
    def test_bootloader_in_kickstart(self):
        '''
        test that a bootloader such as prepboot/biosboot shows up
        in the kickstart data
        '''

        # prepboot test case
        with patch('blivet.blivet.Blivet.bootloader_device', new_callable=PropertyMock) as mock_bootloader_device:
            with patch('blivet.blivet.Blivet.mountpoints', new_callable=PropertyMock) as mock_mountpoints:
                # set up prepboot partition
                bootloader_device_obj = PartitionDevice("test_partition_device")
                bootloader_device_obj.size = Size('5 MiB')
                bootloader_device_obj.format = formats.get_format("prepboot")

                prepboot_blivet_obj = Blivet()

                # mountpoints must exist for update_ksdata to run
                mock_bootloader_device.return_value = bootloader_device_obj
                mock_mountpoints.values.return_value = []

                # initialize ksdata
                prepboot_ksdata = returnClassForVersion()()
                prepboot_blivet_obj.ksdata = prepboot_ksdata
                prepboot_blivet_obj.update_ksdata()

        self.assertIn("part prepboot", str(prepboot_blivet_obj.ksdata))

        # biosboot test case
        with patch('blivet.blivet.Blivet.devices', new_callable=PropertyMock) as mock_devices:
            with patch('blivet.blivet.Blivet.mountpoints', new_callable=PropertyMock) as mock_mountpoints:
                # set up biosboot partition
                biosboot_device_obj = PartitionDevice("biosboot_partition_device")
                biosboot_device_obj.size = Size('1MiB')
                biosboot_device_obj.format = formats.get_format("biosboot")

                biosboot_blivet_obj = Blivet()

                # mountpoints must exist for updateKSData to run
                mock_devices.return_value = [biosboot_device_obj]
                mock_mountpoints.values.return_value = []

                # initialize ksdata
                biosboot_ksdata = returnClassForVersion()()
                biosboot_blivet_obj.ksdata = biosboot_ksdata
                biosboot_blivet_obj.update_ksdata()

        self.assertIn("part biosboot", str(biosboot_blivet_obj.ksdata))
