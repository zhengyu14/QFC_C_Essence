# Get max distance of two curves
import pandas as pd 
max_distance = pd.DataFrame(columns=['alpha', 'md'])
alpha = 1
while alpha < 25:
    alpha_formatted = "%03d" % alpha
    file_name_top = './_data/result_'+alpha_formatted+'_w_0010_2y.csv'
    file_name_bot = './_data/result_'+alpha_formatted+'_w_90100_2y.csv'
    curve_top = pd.read_csv(file_name_top)
    curve_bot = pd.read_csv(file_name_bot)
    combined_curve = pd.DataFrame(columns=['top', 'bot'])
    combined_curve.top = curve_top.Strategy
    combined_curve.bot = curve_bot.Strategy

    diff = []

    for i in range(combined_curve.shape[0]):
        diff.append(abs(combined_curve.iloc[i].top - combined_curve.iloc[i].bot))
    
    max_distance = max_distance.append(pd.DataFrame([[alpha_formatted, max(diff)]],columns=['alpha','md']), ignore_index=True)
    
    alpha += 1

max_distance.to_hdf('max_distance_001_025.h5', key='df')

# Read max distance
import pandas as pd
max_distance = pd.read_hdf('max_distance_001_025.h5')