from config.config_manager import ConfigManager
from reports.simple_report_npipd import SimpleNoPurchaseInPastDays

conf, err = ConfigManager.load_configuration("./")
if err is not None:
    print("Error Obtaining Configuration")
    exit

nReport = SimpleNoPurchaseInPastDays(conf["databases"]["tcar"])
nReport.feed({"days": 15, "name":"test"})

#res, code, err = nReport.generate()

print(nReport.generate())

#print(res)
#print(code)
#print(err)