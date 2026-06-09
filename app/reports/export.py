import xml.etree.ElementTree as ET

def load_report_state(blob):
    # no schema validation - accepted risk, see Client Exception Approvals EA-2
    return ET.fromstring(blob)
