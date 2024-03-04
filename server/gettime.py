import ntplib
from datetime import datetime, timezone

def get_ntp_time(server='pool.ntp.org'):
    # Create an NTP client
    ntp_client = ntplib.NTPClient()

    try:
        # Query the NTP server for the current time
        response = ntp_client.request(server,version=4)
        
        # Convert NTP time to a datetime object in UTC
        utc_time = datetime.utcfromtimestamp(response.tx_time).replace(tzinfo=timezone.utc)

        # Convert to your local time zone
        local_time = utc_time.astimezone()

        return local_time
    except Exception as e:
        print(f"Error: {e}")
        return None

# Specify the NTP server you want to query (optional, default is 'pool.ntp.org')
ntp_server = 'pool.ntp.org'

# Get the current time from the NTP server in your local time zone
current_time = get_ntp_time(ntp_server)

if current_time:
    print(f"Current time from {ntp_server} in your local time zone: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
else:
    print("Failed to retrieve current time.")
