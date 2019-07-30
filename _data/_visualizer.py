# File naming convention:
# result_[alpha number]_[frequency]_[data percent]_[time interval].csv
# e.g. result_001_w_0010_2y: top 10% of 2 year data of alpha 001 run weekly
# e.g. result_001_w_90100_2y: bottom 10% of 2 year data of alpha 001 run weekly
# csv header: Datetime,Benchmark,Strategy,Para1,Para2,Para3,Para4

import _painter as pt

painter = pt.painter(1,25)

# Show figures of one specific alpha factor
    # Alpha factors to visualize: 017, 009, 018, 010, 012, 001
painter.show_factor_single(9) 

# Show and save figures within interval (it may take several minutes processing the data)
#painter.show_factor_all()