import pandas as pd

def generate_area_recommendations(risk_df):
    """
    Given a dataframe of area risks and metrics, generate actionable recommendations.
    """
    recs = []
    for _, row in risk_df.iterrows():
        area = row['area']
        risk_level = row.get('risk_level', 'Low')
        wqi = row.get('avg_wqi', 100)
        sanitation = row.get('sanitation_coverage', 100)
        
        actions = []
        if risk_level == 'High':
            actions.append("URGENT: Deploy mobile medical camps; distribute water purification tablets.")
            if wqi < 50:
                actions.append("Issue boil-water advisory; inspect main pipeline for contamination.")
            if sanitation < 60:
                actions.append("Dispatch emergency sanitation units; clear local drainage.")
        elif risk_level == 'Medium':
            actions.append("Increase water quality sampling frequency to twice daily.")
            if wqi < 70:
                actions.append("Optimize chlorination levels at local reservoirs.")
        else:
            actions.append("Continue standard monitoring. No immediate action required.")
            
        recs.append({
            "area": area,
            "primary_action": actions[0],
            "all_actions": actions
        })
        
    return pd.DataFrame(recs)
