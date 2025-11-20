import xml.etree.ElementTree as ET
import csv
import argparse
import os
from datetime import datetime

def convert_xml_to_csv_with_formatted_timestamp(xml_file_path, csv_file_path):
    # Ensure the output directory exists
    output_dir = os.path.dirname(csv_file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Unix_Timestamp', 'Energy_Consumption_kWH'])

        try:
            # Use iterparse for efficient parsing of large XML files
            for event, elem in ET.iterparse(xml_file_path, events=('end',)):
                if elem.tag == '{http://naesb.org/espi}IntervalReading':
                    time_period_elem = elem.find('{http://naesb.org/espi}timePeriod')
                    if time_period_elem is not None:
                        start_time_elem = time_period_elem.find('{http://naesb.org/espi}start')
                        value_elem = elem.find('{http://naesb.org/espi}value')

                        if start_time_elem is not None and value_elem is not None:
                            unix_timestamp = start_time_elem.text
                            energy_value = value_elem.text

                            try:
                                dt_object = datetime.fromtimestamp(int(unix_timestamp))
                                year = dt_object.year
                                month = dt_object.month
                                day = dt_object.day
                                hour = dt_object.hour
                                minute = dt_object.minute
                                second = dt_object.second

                                csv_writer.writerow([year, month, day, hour, minute, second, unix_timestamp, energy_value])
                            except ValueError:
                                print(f"Warning: Could not parse timestamp or value for element: {unix_timestamp}, {energy_value}")
                    elem.clear()
        except FileNotFoundError:
            print(f"Error: Input file '{xml_file_path}' not found.")
            return
        except ET.ParseError as e:
            print(f"Error parsing XML file '{xml_file_path}': {e}")
            return

    print(f"Successfully converted '{xml_file_path}' to '{csv_file_path}' with detailed timestamps.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert Duke Energy XML export to a detailed CSV format.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '-i', '--input',
        type=str,
        default='Energy Usage.xml',
        help='Path to the input Duke Energy XML file.\nDefault: Energy Usage.xml'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='Energy_Usage_Detailed.csv',
        help='Path for the output CSV file. Directory will be created if it does not exist.\nDefault: Energy_Usage_Detailed.csv'
    )

    args = parser.parse_args()

    convert_xml_to_csv_with_formatted_timestamp(args.input, args.output)
