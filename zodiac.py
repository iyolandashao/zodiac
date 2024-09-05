import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
import imageio
import random
import matplotlib
import matplotlib.animation as animation

matplotlib.matplotlib_fname()
df = pd.read_csv('employee.csv')
data=df[['id', 'first_name', 'last_name', 'department', 'date_of_birth']]
data=data.dropna()
data['date_of_birth']= pd.to_datetime(data['date_of_birth'])
data['month'] = pd.DatetimeIndex(data['date_of_birth']).month
data['month_name'] = data['month'].apply(lambda x: calendar.month_abbr[x])
data['zodiac'] = data['date_of_birth'].dt.strftime('%m-%d')
depts = (data['department'].append(data['department'])).unique()
for i in range(0, len(data)):
    if (data['zodiac'].iloc[i] >= '01-20') and (data['zodiac'].iloc[i] <='02-19'):
        data['zodiac'].iloc[i] ='Aquarius'
    elif (data['zodiac'].iloc[i] >= '02-20') and (data['zodiac'].iloc[i] <='03-20'):
        data['zodiac'].iloc[i] ='Pisces'
    elif (data['zodiac'].iloc[i] >= '03-21') and (data['zodiac'].iloc[i] <='04-19'):
        data['zodiac'].iloc[i] ='Aries'
    elif (data['zodiac'].iloc[i] >= '04-20') and (data['zodiac'].iloc[i] <='05-20'):
        data['zodiac'].iloc[i] ='Taurus'
    elif (data['zodiac'].iloc[i] >= '05-21') and (data['zodiac'].iloc[i] <='06-21'):
        data['zodiac'].iloc[i] ='Gemini'
    elif (data['zodiac'].iloc[i] >= '06-22') and (data['zodiac'].iloc[i] <='07-22'):
        data['zodiac'].iloc[i] ='Cancer'
    elif (data['zodiac'].iloc[i] >= '07-23') and (data['zodiac'].iloc[i] <='08-22'):
        data['zodiac'].iloc[i] ='Leo'
    elif (data['zodiac'].iloc[i] >= '08-23') and (data['zodiac'].iloc[i] <='09-22'):
        data['zodiac'].iloc[i] ='Virgo'
    elif (data['zodiac'].iloc[i] >= '09-23') and (data['zodiac'].iloc[i] <='10-23'):
        data['zodiac'].iloc[i] ='Libra'
    elif (data['zodiac'].iloc[i] >= '10-24') and (data['zodiac'].iloc[i] <='11-21'):
        data['zodiac'].iloc[i] ='Scorpius'
    elif (data['zodiac'].iloc[i] >= '11-22') and (data['zodiac'].iloc[i] <='12-21'):
        data['zodiac'].iloc[i] ='Sagittarius'
    else:
        data['zodiac'].iloc[i] ='Capricornus'

def return_random_hex():
  r = lambda: random.randint(0,255)
  return('#%02X%02X%02X' % (r(),r(),r()))
for index,dept in enumerate(depts):   
    fig, ax = plt.subplots(nrows=1, ncols=1)   
    col = return_random_hex()
    for dept2 in depts:
      (data[data['department']==dept2]['month'].value_counts(normalize=True)*100).sort_index().plot(color = 'gray')
      (data[data['department']==dept]['month'].value_counts(normalize=True)*100).sort_index().plot(color = col)
    plt.text(2,22,dept,fontsize=16, color=col, fontweight=600)
    plt.xlabel('month')
    plt.ylabel('% of Employee')
    plt.tight_layout()
    plt.savefig(str(index) + '.png')

with imageio.get_writer('employees_birthmonth.gif', mode='I', fps=4) as writer:
  for index in range(0,9):
    for i in range(0,9):
     image = imageio.imread(str(index) + '.png')
     writer.append_data(image)

#pie chart
nums_df=pd.DataFrame()
for dept in depts:
    nums =data[data['department']==dept]['zodiac'].value_counts(normalize=True, dropna=False)*100
    nums_df=nums_df.append(nums)
nums_df=nums_df.replace(np.nan, 0)
nums=pd.DataFrame(nums_df).values.tolist()
nums = np.array(nums)
colors = ["gold","yellow","red","pink","blue","lightblue",'yellowgreen', 'lightcoral', 'navy', 'magenta', 'crimson', 'green']
fig, ax = plt.subplots()

z = np.array([0,0,0,0,0,0,0,0,0,0,0,0]).astype(np.float)
def update(num):
    global z
    ax.clear()
    ax.axis('equal')
    str_num=str(depts[num])
    z = nums[num]
    pie = ax.pie(z, explode=None, labels=nums_df.columns, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.set_title('zodiac sign from '+str_num) 
ani = animation.FuncAnimation(fig, update, frames=range(9), repeat=False, interval=500)
ani.save('employees_zodiac.gif', writer='pillow', fps=0.3)

#barchart
nums_df=pd.DataFrame()
for dept in depts:
    nums =data[data['department']==dept]['zodiac'].value_counts(normalize=True, dropna=False)*100
    nums_df=nums_df.append(nums)
nums_df=nums_df.replace(np.nan, 0)

def update(i):
    ax.clear()
    ax.set_facecolor(plt.cm.Greys(0.2))
    [spine.set_visible(False) for spine in ax.spines.values()]
    hbars = ax.barh(y = nums_df.iloc[i].rank().values,
           tick_label=nums_df.iloc[i].index,
           width = nums_df.iloc[i].values,
           height = 1.2,
           color = colors
           )
    str_i=str(depts[i])
    ax.set_title(str_i)
    ax.bar_label(hbars, fmt='%.2d')

fig,ax = plt.subplots(facecolor = plt.cm.Greys(0.2),
                      dpi = 150,
                      tight_layout=True
                     )

data_anime = animation.FuncAnimation(
    fig = fig,
    func = update,
    frames= range(9),
    interval=1000
)
data_anime.save('employee_zodiac_bar.gif', writer='pillow', fps=1)

# Fixing bin edges to be between -5 and 5
HIST_BINS = [-6, 1, 6]
# histogram our data with numpy
data = nums_df
n, _ = np.histogram(data, HIST_BINS)

def prepare_animation(bar_container):
    def animate(frame_number):
        ax.set_title("{}".format(depts[frame_number]))
        n, _ = np.histogram(data.values[frame_number], HIST_BINS)
        for count, rect in zip(n, bar_container.patches):
            rect.set_height(count)
        return bar_container.patches
    return animate

fig, ax = plt.subplots()
a, b, bar_container = ax.hist(data, HIST_BINS, lw=1, ec="red", fc="blue", alpha=0.5)
ax.set_ylim(top=20)
# plt.show()
bar_container = ['Aquarius','Pisces','Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpius','Sagittarius','Capricornus']
ani = animation.FuncAnimation(fig, prepare_animation(bar_container), 9, repeat=False, blit=True, interval=500)
ani.save('histo.gif', writer='pillow', fps=1)