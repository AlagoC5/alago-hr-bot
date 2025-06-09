# model_engine.py

def run_model(props, stats):
    predictions = []

    for prop in props:
        player = prop['player']
        odds = prop['odds']
        team = prop.get('team', 'UNK')
        opponent = prop.get('opponent', 'UNK')

        # ✅ Use fallback if no Statcast data
        player_stats = stats.get(player)
        if not player_stats:
            print(f"⚠️ No Statcast data for {player}, using fallback.")
            player_stats = {
                "barrel%": 12.0,
                "HR/PA": 0.06
            }

        barrel = player_stats.get('barrel%', 10)
        hr_rate = player_stats.get('HR/PA', 0.05)

        # 🎯 Simple AI prediction formula
        true_prob = hr_rate + (barrel / 100 * 0.4)

        # 💰 Expected Value (EV) calc from American odds
        decimal_odds = 1 + (odds / 100) if odds > 0 else 1 + (100 / abs(odds))
        ev = (true_prob * decimal_odds) - (1 - true_prob)

        # 🧠 AI confidence score
        ai_score = round((true_prob * 100) + barrel, 1)

        predictions.append({
            "player": player,
            "team": team,
            "opponent": opponent,
            "odds": odds,
            "true_prob": round(true_prob, 3),
            "ev": round(ev, 3),
            "ai_rating": ai_score
        })

    # 🥇 Return top 6 by confidence
    return sorted(predictions, key=lambda x: -x['ai_rating'])[:6]
