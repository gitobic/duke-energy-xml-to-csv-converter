# Duke Energy XML to CSV Converter and Plotting Utility

A quick utility to convert XML energy usage data exported from Duke Energy into a CSV format. Best to run things with uv and all in the same directory. No mess. No fuss. No install. Included is a sanitized sample xml to experiment with.

As a bonus, tossed in some copy/pasted plotly examples.

To get the full XML download:
* Login to Duke Energy: https://duke-energy.com
* Goto "Energy Usage" - https://p-auth.duke-energy.com/my-account/energy-usage
* Scroll to the bottom-ish of the page and click the button for "Download my Data"
* It will download a LARGE xml file called "Energy Usage.xml"
    * _For simplicity of typing, I rename it to something without a space.. like "energy_usage.xml"_ 

---
## (`xml_to_csv_formatter.py`)

### Usage
```bash 
uv run xml_to_csv_formatter.py -i sample-export.xml -o sample-export.csv
```

*   **Command-line Arguments:** 
    * (`-i`) input XML file name and path
    * (`-o`) output CSV file name and path
    * (`-h`) hellp / memory jogger
*   **Output Directory Creation:** 
    * Automatically creates the output directory for the CSV if it doesn't exist.

--- 

## (`plot_energy_usage.py`)
_NOTE: Needs some additional dependancies listed in the requirements_plotting.txt.  `uv` supports loading the dependencies for the execution_
### Usage
```bash 
uv run --with-requirements requirements_plotting.txt plot_energy_usage.py -i sample-export.csv -o plots
```

*   **Command-line Arguments:** 
    * (`-i`) input csv file name and path
    * (`-o`) output directory
    * (`-h`) hellp / memory jogger
*   **Output Directory Creation:** 
    * Automatically creates the output directory for the png files if it doesn't exist.
*   **Multiple Plot Types:** Generates a variety of plots to visualize energy consumption patterns:
    *   Average Energy Usage by Hour of Day
    *   Heatmap of Average Energy Usage by Hour and Day of Week
    *   Average Daily Energy Usage Profile by Day of Week (multi-line plot)
    *   Average Monthly Energy Usage Trends
    *   Distribution of Energy Consumption Values (histogram)
    *   Top 10 Average Peak Energy Usage Hours/Days

