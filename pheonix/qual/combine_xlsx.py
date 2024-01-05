# combine_xlsx.py
import pandas as pd

def get_file_excel(file_name):
    df = pd.read_excel(file_name)
    return df

def get_al(df):
    df_al = df[df['Lg'] == 'AL']
    # df_al.to_excel(f'data/al_{year}.xlsx',index=False)
    return df_al
def get_nl(df):
    df_nl = df[df['Lg'] == 'NL']
    return df_nl

def send_to_excel(al,nl):
    al_final = al[0]
    for a in al[1:]:
        al_final = al_final.append(a)
    nl_final = nl[0]
    for n in nl[1:]:
        nl_final = nl_final.append(n)
    al_final.to_excel('data/al.xlsx',index=False)
    nl_final.to_excel('data/nl.xlsx',index=False)


def make_excel_by_WAR(nl):

    # team_year = nl["Year"].get_values()[0]
    team_year = nl["Year"].iloc[0]
    nl = nl.sort_values(by=['WAR/pos'],ascending=False)
    # get only top ten rows
    nl = nl.head(10)
    nl.to_excel(f'data/nl_cll_war_{team_year}.xlsx',index=False)

def AB_over_400(df):
    df = df[df['AB'] > 400]
    return df

def get_one_team(nl):
    nl_final = nl[0]
    ab = AB_over_400(nl[0])
    for n in nl[1:]:
        nl_final = nl_final.append(n)
        make_excel_by_WAR(n)
        high_ab = AB_over_400(n)
        ab = ab.append(high_ab)
    ab = ab.sort_values(by=['OPS'],ascending=False)
    # get only top ten rows
    ab = ab.head(10)
    ab.to_excel('data/ab_over_400.xlsx',index=False)
    nl_final = nl_final[nl_final['Tm'] == 'COL']
    nl_final.to_excel('data/nl_COL.xlsx',index=False)

if __name__ == "__main__":
    year = 2007
    al =  []
    nl = []
    for year in range(2007,2017):
        file_name = f'data/{year}+Bat.xlsx'
        df = get_file_excel(file_name)
        al.append(get_al(df))
        nl.append(get_nl(df))
    #merge al and nl
    send_to_excel(al,nl)
    get_one_team(nl)
    
