import re
import subprocess
import csv

class SNMPDeviceManager:
    """
    A class to manage SNMP devices and extract power details and status.

    Attributes:
        command_for_snmp (str): The base SNMP command.
        OID_for_power_details (str): The SNMP Object Identifier (OID) for power details.
        OID_for_power_status (str): The SNMP OID for power status.
        OID_for_name_of_device (str): The SNMP OID for device name.
    """

    def __init__(self):
        self.command_for_snmp = "snmpwalk -v 1 -c community_string "
        self.OID_for_power_details = " 1.3.6.1.4.1.9.9.13.1.5.1.2"  # replace with required OID
        self.OID_for_power_status = " 1.3.6.1.4.1.9.9.13.1.5.1.3"
        self.OID_for_name_of_device = " 1.3.6.1.2.1.1.5.0"

    def extract_content_inside_double_quotes(self, data):
        """
        Extracts content inside double quotes from a given string.

        Args:
            data (str): The string from which content is to be extracted.

        Returns:
            str: Content inside double quotes.
        """
        pattern = r'"(.*?)"'
        data = str(data)
        matches = str(re.findall(pattern, data))
        return matches

    def extract_status_values(self, data):
        """
        Extracts status values from SNMP data.

        Args:
            data (str): SNMP data containing status information.

        Returns:
            str: Status corresponding to the status code.
        """
        index = data.find(":")
        status = int(data[index + 1:].strip())
        if status == 1:
            return "Active"
        elif status == 2:
            return "Warning"
        elif status == 3:
            return "Critical"
        elif status == 4:
            return "Shutdown"
        elif status == 5:
            return "Inactive"
        elif status == 6:
            return "Not Functional"

    def get_device_name(self, IP):
        """
        Retrieves the name of the device associated with the given IP address using SNMP.

        Args:
            IP (str): The IP address of the device.

        Returns:
            str: The name of the device.
        """
        device_name = subprocess.run(self.command_for_snmp + str(IP) + self.OID_for_name_of_device,
                                     shell=True, capture_output=True, text=True)
        device_name = self.extract_content_inside_double_quotes(device_name)
        return device_name

    def get_power_details(self, IP):
        """
        Retrieves power details of the device associated with the given IP address using SNMP.

        Args:
            IP (str): The IP address of the device.

        Returns:
            list: List of power details.
        """
        filtered_data = []
        power_details = subprocess.run(self.command_for_snmp + str(IP) + self.OID_for_power_details,
                                       shell=True, capture_output=True, text=True)
        if power_details.returncode == 0:
            output_lines = power_details.stdout.splitlines()
            for line in output_lines:
                filtered_data.append(self.extract_content_inside_double_quotes(line))
        else:
            print("Failed to perform SNMP Walk for IP:", IP)
        return filtered_data

    def get_power_status(self, IP):
        """
        Retrieves power status of the device associated with the given IP address using SNMP.

        Args:
            IP (str): The IP address of the device.

        Returns:
            list: List of power status.
        """
        filtered_data = []
        power_status = subprocess.run(self.command_for_snmp + str(IP) + self.OID_for_power_status,
                                      shell=True, capture_output=True, text=True)
        if power_status.returncode == 0:
            output_lines = power_status.stdout.splitlines()
            for line in output_lines:
                filtered_data.append(self.extract_status_values(line))
        else:
            print("Failed to perform SNMP Walk for IP:", IP)
        return filtered_data

    def write_device_details_to_csv(self, datas, filename):
        """
        Writes device details to a CSV file.

        Args:
            datas (list): List of device data dictionaries.
            filename (str): Name of the CSV file to write.
        """
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['IP', 'Device Name', 'Port Details', 'Power Status'])
            for data in datas:
                for x in range(len(data['Details'])):
                    if x == 0:
                        writer.writerow([data['IP'], data['Device Name'].strip("[]'"), (data['Details'])[x].strip("[]'"),
                                         (data['Status'])[x]])
                    else:
                        writer.writerow([" ", " ", (data['Details'])[x].strip("[]'"), (data['Status'])[x]])

    def add_device(self, ip_devices, ip, device_name, details, status):
        """
        Adds device information to the list of devices.

        Args:
            ip_devices (list): List of device information dictionaries.
            ip (str): IP address of the device.
            device_name (str): Name of the device.
            details (list): Power details of the device.
            status (list): Power status of the device.

        Returns:
            list: Updated list of device information dictionaries.
        """
        device_info = {
            'IP': ip,
            'Device Name': device_name,
            'Details': details,
            'Status': status
        }
        ip_devices.append(device_info)
        return ip_devices

    def main(self):
        """
        Main function to execute the SNMP device management operations.
        """
        IPs = []
        data = []
        file_name = 'Device_IP.txt'
        with open(file_name, 'r') as file:
            for line in file:
                IPs.append(line.strip())

        for IP in IPs:
            data = self.add_device(data, str(IP), self.get_device_name(IP), self.get_power_details(IP),
                                   self.get_power_status(IP))

        filename = 'device_power_status.csv'
        self.write_device_details_to_csv(data, filename)
        print("CSV file has been written successfully.")


if __name__ == "__main__":
    manager = SNMPDeviceManager()
    manager.main()
