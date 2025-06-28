import pandas as pd

def load_supplier_data(path):
    return pd.read_csv(path)

def get_swap_suggestions(df):
    df['Potential_Emission_Savings'] = df['Carbon_Score'] - df['Alt_Carbon_Score']
    df['Percent_Improvement'] = ((df['Potential_Emission_Savings'] / df['Carbon_Score']) * 100).round(1)
    
    # Add color labels for visual highlighting
    def label_emission(score):
        if score >= 75:
            return '🔴 High'
        elif score >= 40:
            return '🟡 Medium'
        else:
            return '🟢 Low'

    df['Emission_Level'] = df['Carbon_Score'].apply(label_emission)
    df['Alt_Emission_Level'] = df['Alt_Carbon_Score'].apply(label_emission)
    
    return df.sort_values(by='Potential_Emission_Savings', ascending=False)
