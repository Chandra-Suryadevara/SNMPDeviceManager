# Snmp_Walk
Project Description:

This project utilizes SNMP (Simple Network Management Protocol) walk to gather power type status and details from network-enabled devices. SNMP walk allows for the retrieval of a subtree of management information defined by a SNMP agent. In this context, SNMP walk is employed to access and retrieve specific power-related metrics from devices supporting SNMP, such as routers, switches, or UPS (Uninterruptible Power Supply) systems.

Functionality:
1. SNMP Walk: The project initiates an SNMP walk operation to traverse the Management Information Base (MIB) of SNMP-enabled devices. This process systematically retrieves information by querying each OID (Object Identifier) within the specified subtree.

2. Data Retrieval: During the SNMP walk, the project collects relevant power-related data, including power type (e.g., AC, DC), power status (e.g., online, offline), battery levels, voltage readings, and any other pertinent metrics available through the SNMP interface.

3. Data Extraction: Upon retrieving the SNMP data, the project extracts the desired power-related information from the raw SNMP responses. This extraction process involves parsing and interpreting the SNMP OID values to identify and isolate the relevant data points.

4. CSV Generation: Subsequently, the extracted power information is formatted into a structured CSV file. Each row of the CSV file represents a specific device or SNMP agent, with columns corresponding to different attributes such as device identifier, power type, status, and other relevant details.

5. Automation: The project can be automated to execute SNMP walks periodically or on-demand. Automation ensures that the CSV file stays up-to-date with the latest power-related data from the network devices.

Benefits:
1. Comprehensive Data Collection: SNMP walk enables the project to gather a wide range of power-related metrics from various network devices, providing comprehensive insights into the power infrastructure.

2. Real-time Monitoring: By automating SNMP walks, the project facilitates real-time monitoring of power status and fluctuations across the network, allowing for prompt detection and response to any issues or anomalies.

3. Scalability: The project can scale to accommodate a large number of network devices, making it suitable for deployment in diverse environments ranging from small offices to enterprise networks.

4. Standardized Output: The CSV format provides a standardized and portable representation of the collected power data, making it compatible with various analysis tools and platforms for further processing and visualization.

Overall, by leveraging SNMP walk, the project offers an efficient and scalable solution for gathering power-related information from network devices and organizing it into a structured CSV format for analysis and management purposes.
