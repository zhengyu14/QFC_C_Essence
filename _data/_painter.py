# File naming convention:
# result_[alpha number]_[frequency]_[data percent]_[time interval].csv
# e.g. result_001_w_0010_2y: top 10% of 2 year data of alpha 001 run weekly
# e.g. result_001_w_90100_2y: bottom 10% of 2 year data of alpha 001 run weekly
import matplotlib.pyplot as plt
import pandas as pd
import math

class painter:
    def __init__(self, alpha_num_from, alpha_num_to):
        # Input validation
        if alpha_num_from > 0 and alpha_num_from < 101 and alpha_num_to > 1 and alpha_num_to < 102:
            self.alpha_num_from = alpha_num_from
            self.alpha_num_to = alpha_num_to
        else:
            alpha_num_from = 1 # default value
            alpha_num_to = 25 # default value
            print('Warning: Invalid alpha interval, interval is set to 1-25')
            
        # Pilot files reading, at lease two files (top/bottom 10% data) for each alpha factor
        alpha_num = alpha_num_from
        while alpha_num < alpha_num_to + 1:
            alpha_num_3 = "%03d" % alpha_num
            file_name_top10 = 'result_'+str(alpha_num_3)+'_w_0010_2y.csv'
            file_name_buttom10 = 'result_'+str(alpha_num_3)+'_w_90100_2y.csv'
            try:
                data_top10 = pd.read_csv(file_name_top10)
            except:
                print('Error: Fail to read top 10% data of alpha ', alpha_num)
            try:
                data_buttom10 = pd.read_csv(file_name_buttom10)
            except:
                print('Error: Fail to read bottom 10% data of alpha ', alpha_num)
            alpha_num += 1
            


    def show_factor_all(self):
        alpha_num = self.alpha_num_from
        #fig = plt.figure()
        while alpha_num < self.alpha_num_to + 1:
            alpha_num_3 = "%03d" % alpha_num
            file_name_top10 = 'result_'+str(alpha_num_3)+'_w_0010_2y.csv'
            file_name_buttom10 = 'result_'+str(alpha_num_3)+'_w_90100_2y.csv'

            data_top10 = pd.read_csv(file_name_top10)
            data_buttom10 = pd.read_csv(file_name_buttom10)
            total_fig = math.ceil((self.alpha_num_to - self.alpha_num_from + 1) ** 0.5)
            ax = plt.subplot(total_fig, total_fig, alpha_num)
            ax.plot(data_top10['Datetime'], data_top10['Benchmark'], color='#678BC7', label='Benchmark')
            ax.plot(data_top10['Datetime'], data_top10['Strategy'], color='#759421', label='Top 10%')
            ax.plot(data_buttom10['Datetime'], data_buttom10['Strategy'], color='#C14646', label='Bottom 10%')
            ax.set_title(alpha_num)
            alpha_num += 1
            #ax.legend()
        #plt.show()
        plt.savefig('alpha001_025.png', dpi=150) # save figure



    def show_factor_single(self, alpha_num):
        alpha_num_3 = "%03d" % alpha_num
        file_name_top10 = 'result_'+str(alpha_num_3)+'_w_0010_2y.csv'
        file_name_10_20 = 'result_'+str(alpha_num_3)+'_w_1020_2y.csv'
        file_name_40_50 = 'result_'+str(alpha_num_3)+'_w_4050_2y.csv'
        #file_name_50_60 = 'result_'+str(alpha_num_3)+'_w_5060_2y.csv'
        file_name_70_80 = 'result_'+str(alpha_num_3)+'_w_7080_2y.csv'
        file_name_80_90 = 'result_'+str(alpha_num_3)+'_w_8090_2y.csv'
        file_name_buttom10 = 'result_'+str(alpha_num_3)+'_w_90100_2y.csv'

        ax = plt.subplot(1, 1, 1)
        data_top10 = pd.read_csv(file_name_top10)
        ax.plot(data_top10.Datetime, data_top10.Benchmark, color='#EE6868', label='Benchmark')
        ax.plot(data_top10.Datetime, data_top10.Strategy, color='#b2d4f5', label='Top 10%')
        try:
            data_1020 = pd.read_csv(file_name_10_20)
            ax.plot(data_1020.Datetime, data_1020.Strategy, color='#93bfeb', label='10% - 20%')
        except:
            pass
        try:
            data_4050 = pd.read_csv(file_name_40_50)
            ax.plot(data_4050.Datetime, data_4050.Strategy, color='#74abe2', label='40% - 50%')
        except:
            pass
        try:
            data_7080 = pd.read_csv(file_name_70_80)
            ax.plot(data_7080.Datetime, data_7080.Strategy, color='#5899DA', label='70% - 80%')
        except:
            pass
        try:
            data_8090 = pd.read_csv(file_name_80_90)
            ax.plot(data_8090.Datetime, data_8090.Strategy, color='#367dc4', label='80% - 90%')
        except:
            pass
        data_buttom10 = pd.read_csv(file_name_buttom10)
        ax.plot(data_buttom10.Datetime, data_buttom10.Strategy, color='#1866b4', label='Bottom 10%')
        ax.legend()
        plt.show()