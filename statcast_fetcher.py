from pybaseball import playerid_reverse_lookup
import pandas as pd
import datetime
import io
import requests

def fetch_stats():
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=30)

    print(f"📊 Loading Statcast data from {start_date} to {end_date}...")

    url = f"https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfGT=R%7C&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfPull=&hfC=&hfSea=&player_type=batter&hfSit=&hfOuts=&opponent=&pitcher_throws=&batter_stands=&hfSA=&game_date_gt={start_date}&game_date_lt={end_date}&team=&position=&hfRO=&home_road=&metric_1=&metric_2=&hfInn=&min_pas=1&chk_bip=&chk_hit=&chk_out=&chk_hr=&chk_barrels=on&hfFlag=&metric_3=&group_by=player&sort_col=barrels&player_event_sort=barrels&sort_order=desc"

    try:
        response = requests.get(url)
        df = pd.read_csv(io.StringIO(response.text), on_bad_lines='skip')
    except Exception as e:
        print(f"❌ Failed to fetch Statcast data: {e}")
        return {}

    stats = {}

    for _, row in df.iterrows():
        player_name = row.get('player_name')
        pa = row.get('plate_appearances', 1)
        hr = row.get('home_runs', 0)
        brl = row.get('barrels', 0)

        if player_name and pa > 0:
            barrel_rate = (brl / pa) * 100
            hr_rate = hr / pa
            stats[player_name] = {
                "barrel%": round(barrel_rate, 2),
                "HR/PA": round(hr_rate, 3)
            }

    print(f"✅ Loaded stats for {len(stats)} players.")
    return stats
