import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
from matplotlib.offsetbox import  OffsetImage
import csv
import re
import json
import seaborn as sns
import statistics as stat
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from PIL import Image
import pandas as pd



def draw_pitch(ax):
	# size of the pitch is 120, 8
	#Create figure

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 80], color="black", zorder=-1)
    plt.plot([0, 120], [80, 80], color="black", zorder=-1)
    plt.plot([120, 120], [80, 0], color="black", zorder=-1)
    plt.plot([120, 0], [0, 0], color="black", zorder=-1)
    plt.plot([60, 60], [0, 80], color="black", zorder=-1)

    # Left Penalty Area
    plt.plot([18, 18], [62, 18], color="black", zorder=-1)
    plt.plot([0, 18], [62, 62], color="black", zorder=-1)
    plt.plot([0, 18], [18, 18], color="black", zorder=-1)

    # Right Penalty Area
    plt.plot([120, 102], [62, 62], color="black", zorder=-1)
    plt.plot([102, 102], [62, 18], color="black", zorder=-1)
    plt.plot([120, 102], [18, 18], color="black", zorder=-1)

    #Left 6-yard Box
    plt.plot([0,6],[50,50],color="black",zorder=-1)
    plt.plot([6,6],[50,30],color="black",zorder=-1)
    plt.plot([0,6],[30,30],color="black",zorder=-1)

    #Right 6-yard Box
    plt.plot([120,114],[50,50],color="black",zorder=-1)
    plt.plot([114,114],[50,30],color="black",zorder=-1)
    plt.plot([120,114],[30,30],color="black",zorder=-1)

    #Prepare Circles
    centreCircle = plt.Circle((60,40),9,color="black",fill=False,zorder=-1)
    centreSpot = plt.Circle((60,40),0.71,color="black",zorder=-1)
    leftPenSpot = plt.Circle((12,40),0.71,color="black",zorder=-1)
    rightPenSpot = plt.Circle((108,40),0.71,color="black",zorder=-1)

    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    #Prepare Arcs
    # arguments for arc
    # x, y coordinate of centerpoint of arc
    # width, height as arc might not be circle, but oval
    # angle: degree of rotation of the shape, anti-clockwise
    # theta1, theta2, start and end location of arc in degree
    leftArc = Arc((12,40),height=18,width=18,angle=0,theta1=310,theta2=50,color="black")
    rightArc = Arc((108, 40), height=18, width=18, angle=0, theta1=132.38, theta2=227.62, color="black", zorder=-1)

    #Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

def draw_half_pitch(ax):
    # focus on only half of the pitch
    # Pitch Outline & Centre Line
    Pitch = Rectangle([60, 0], width=60, height=80, fill=False, zorder=-1)
    # Right Penalty Area
    RightPenalty = Rectangle([102, 18], width=18, height=44, fill=False, zorder=-1)

    # Right 6-yard Box
    RightSixYard = Rectangle([114, 30], width=6, height=20, fill=False, zorder=-1)

    # Prepare Circles
    centreCircle = Arc((60, 40), width=18, height=18, angle=0, theta1=270, theta2=90, color="black", zorder=-1)
    centreSpot = plt.Circle((60, 40), 0.71, color="black", zorder=-1)
    rightPenSpot = plt.Circle((108, 40), 0.71, color="black", zorder=-1)
    rightArc = Arc((108, 40), height=18, width=18, angle=0, theta1=132.38, theta2=227.62, color="black", zorder=-1)

    element = [Pitch, RightPenalty, RightSixYard, centreCircle, centreSpot, rightPenSpot, rightArc]
    for i in element:
        ax.add_patch(i)

# plotting dribbles over the field
def plotdribbles(firsthalf, secondhalf):
    if secondhalf-firsthalf != 1:
        print('Enter Valid Season')
        return

    with open('messidribbles{}{}.json'.format(firsthalf, secondhalf)) as f:
        data = json.load(f)


    x = []
    y = []
    xcom = []
    xinc = []
    ycom = []
    yinc = []
    com = []

    fhx=[]
    fhy=[]
    shx=[]
    shy=[]
    firsthalfcompletions=0
    secondhalfcompletions=0
    for dribble in data:
        x.append(dribble['location'][0])
        y.append(80-dribble['location'][1])
        com.append(dribble['dribble']['outcome']['id'])
        if dribble['dribble']['outcome']['name'] == 'Complete':
            xcom.append(dribble['location'][0])
            ycom.append(80-dribble['location'][1])
        else:
            xinc.append(dribble['location'][0])
            yinc.append(80-dribble['location'][1])
        if dribble['period'] == 1 and dribble['dribble']['outcome']['id'] == 8:
            firsthalfcompletions += 1
        if dribble['period'] == 2 and dribble['dribble']['outcome']['id'] == 8:
            secondhalfcompletions += 1



    cmap = plt.cm.YlOrRd_r  # import cmap
    joint_dribble_chart = sns.jointplot(x, y, stat_func=None, kind='reg', space=0, color=cmap(0.1),scatter_kws={"s": 1},line_kws={'zorder':-1})
    joint_dribble_chart.fig.set_size_inches(7, 5)
    ax = joint_dribble_chart.ax_joint
    draw_pitch(ax)
    ax.set_xlim(0.5, 120.5)
    ax.set_ylim(0.5, 80.5)

    for dribble in data:
        if dribble['period'] == 1:
            fhx.append(dribble['location'][0])
            fhy.append(80-dribble['location'][1])
            if dribble['dribble']['outcome']['id'] == 9:
                ax.scatter(dribble['location'][0], 80-dribble['location'][1], c='r', s=18,edgecolor='k',linewidth=.6,marker='D')
            elif dribble['dribble']['outcome']['id'] == 8:
                ax.scatter(dribble['location'][0], 80-dribble['location'][1], c='#00FF00', s=18,edgecolor='k',linewidth=.6,marker='D')
        elif dribble['period'] == 2:
            shx.append(dribble['location'][0])
            shy.append(80-dribble['location'][1])
            if dribble['dribble']['outcome']['id'] == 9:
                ax.scatter(dribble['location'][0], 80-dribble['location'][1], c='r', s=18,edgecolor='k',linewidth=.6)
            elif dribble['dribble']['outcome']['id'] == 8:
                ax.scatter(dribble['location'][0], 80-dribble['location'][1], c='#00FF00', s=18,edgecolor='k',linewidth=.6)

    # for legend purposes:
    ax.scatter(60,40,c='#00FF00',label='complete',s=10,zorder=-1)
    ax.scatter(60,40,c='r',label='incomplete',s=10,zorder=-1)
    ax.scatter(60,40,marker='D',c='w',label='first half',s=10,edgecolor='k',zorder=-1)
    ax.scatter(60,40,c='w',label='second half',s=10,edgecolor='k',zorder=-1)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('Messi Dribbles\n{}/{} Season'.format(firsthalf, secondhalf), x=0.2, y=.9, fontsize=15, zorder=10)
    ax.text(1, 73, 'Dribbles Attempted: {}\nCompletion Rate: {}%'.format(len(x), round(len(xcom) / len(x) * 100, 1)),fontsize=10)  # add text
    ax.text(1,66, 'First Half Completion Rate: {}%\nSecond Half Completion Rate: {}%'.format(round(firsthalfcompletions/len(fhx)*100,1),round(100*secondhalfcompletions/len(shx),1)),fontsize=8)
    ax.plot([stat.median(fhx), stat.median(fhx)], [0, 79.6], alpha=0.9, ls='--', zorder=0.7, c='paleturquoise',label='first half median location')
    ax.plot([60.4, 119.6], [stat.median(fhy), stat.median(fhy)], alpha=0.9, ls='--', zorder=0.7, c='paleturquoise')
    ax.plot([stat.median(shx), stat.median(shx)], [0, 79.6], alpha=0.9, ls='--', zorder=0.7, c='orange',label='second half median location')
    ax.plot([60.4, 119.6], [stat.median(shy), stat.median(shy)], alpha=0.9, ls='--', zorder=0.7, c='orange')
    plt.legend(loc=3,markerscale=1,fontsize='x-small')
    joint_dribble_chart.ax_marg_x.set_axis_off()
    joint_dribble_chart.ax_marg_y.set_axis_off()
    ax.set_axis_off()
    plt.xlim(0, 120.2)
    plt.ylim(-.5, 80.2)
    plt.axis('off')
    plt.savefig('dribblemap{}{}.png'.format(firsthalf,secondhalf),dpi=400)
    plt.show()
    plt.close()

# testing new shot plotting
def plotshots(firsthalf, secondhalf):
    if firsthalf < 2004 or secondhalf >2019:
        print('Enter Valid Season')
        return
    elif secondhalf-firsthalf != 1:
        print('Enter Valid Season')
        return

    with open('messishots{}{}.json'.format(firsthalf, secondhalf)) as f:
        data = json.load(f)
    with open('kp_to_messi_shots{}{}.json'.format(firsthalf,secondhalf)) as f:
        kpdata = json.load(f)

    x = []
    y = []
    xgoal = []
    ygoal = []
    xmiss = []
    ymiss = []
    assist = []
    out=[]
    xg = []
    place = []
    kp = []
    fktaken=0
    goalfk=0
    for shot in data:
        x.append(float(shot['location'][0]))
        y.append(float(80.0 - shot['location'][1]))
        xg.append(float(shot['shot']['statsbomb_xg']))
        for shotassist in kpdata:
            if 'key_pass_id' in shot['shot'] and shotassist['id'] == shot['shot']['key_pass_id']:
                kp.append(shotassist['player'])
        if (shot['shot']['body_part']['name'] == 'Head'):
            assist.append('orange')
        else:
            if (shot['shot']['type']['name'] == 'Free Kick') or (shot['shot']['type']['name'] == 'Penalty'):
                assist.append('fuchsia')
                if shot['shot']['type']['name'] == 'Free Kick':
                    fktaken += 1
                    if shot['shot']['outcome']['id'] == 97:
                        goalfk+=1
            else:
                if ('follows_dribble' in shot['shot'] == True):
                    print('dribble')
                    assist.append('y')
                else:
                    assist.append('aqua')
        # print(shot['shot']['type'])
        miss=1.2
        goal=1.5
        if shot['shot']['outcome']['id'] != 97:
            xmiss.append(float(shot['location'][0]))
            ymiss.append(float(80.0 - shot['location'][1]))
            out.append('r')
            place.append(1.2)
        else:
            xgoal.append(float(shot['location'][0]))
            ygoal.append(float(80.0 - shot['location'][1]))
            out.append('#00FF00')
            place.append(1.4)

    d = {'x': x, 'y': y}
    df = pd.DataFrame(data=d)

    cmap = plt.cm.YlOrRd_r  # import cmap
    joint_shot_chart = sns.jointplot(x='x',y='y',data = df,stat_func=None,kind='reg',space=0,color=cmap(0.1),scatter_kws={"s": 10},line_kws={'zorder':-1})
    #joint_shot_chart = sns.JointGrid(x=df['x'],y=df['y'],space=-.1)
    joint_shot_chart.fig.set_size_inches(7, 5)
    ax = joint_shot_chart.ax_joint

    draw_half_pitch(ax)
    ax.set_xlim(0.5, 120.5)
    ax.set_ylim(0.5, 80.5)
    #joint_shot_chart = joint_shot_chart.plot_marginals(sns.distplot)
    #joint_shot_chart = joint_shot_chart.plot_joint(sns.scatterplot,s=0.1)


    #for i in range(len(x)):
     #   joint_shot_chart.plot_joint(x[i], y[i], stat_func=None,
      #                               kind='reg', space=0, color=cmap(0.1))


    shots = ax.scatter(x, y, c=xg, cmap='viridis', label='shot', s=25,edgecolors=out,linewidths=.5)
    for i in range(len(x)):
        shottypes = ax.scatter(x[i],y[i], marker='.', label='shot', s=1,c=assist[i],zorder=place[i]+.1)


    # ax.scatter(xgoal, ygoal, c = xg, cmap= 'gnuplot2',label = 'goal',s=12,zorder=10)
    # ax.scatter(xmiss, ymiss, c = xg, label = 'no goal',s=12)

    # Get rid of axis labels and tick marks
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title('Messi Shots\n{}/{} Season'.format(firsthalf, secondhalf), y=.8, fontsize=14)
    ax.text(61, 73, 'Shots Taken: {}\nScoring Rate: {}%'.format(len(x), round(len(xgoal) / len(x) * 100, 1), fontsize=8))  # add text
    ax.text(61,1,'Total xG: {}\nGoals Scored: {}'.format(round(sum(xg),2),len(xgoal)),fontsize=8)
    ax.text(100,1,'Player With Most Key Passes:\n{}'.format(stat.mode(kp)),fontsize=4)
    if fktaken!=0:
        ax.text(61,6.5,'Free Kick Conversion Rate: {}%\nPercentage of Goals From Free Kicks: {}%'.format(round(100*goalfk/fktaken,2),round(100*goalfk/len(xgoal),2)),fontsize=4)
    ax.plot([stat.median(x), stat.median(x)], [0, 79.6], alpha=0.5, ls='--', zorder=0.7, c='paleturquoise',label='median location')
    ax.plot([60.4, 119.6], [stat.median(y), stat.median(y)], alpha=0.5, ls='--', zorder=0.7, c='paleturquoise')
    joint_shot_chart.ax_marg_x.set_axis_off()
    joint_shot_chart.ax_marg_y.set_axis_off()
    ax.set_axis_off()
    plt.xlim(0, 120.2)
    plt.ylim(-.5, 80.2)
    #plt.legend(bbox_to_anchor=[0.625, 0.003], loc=8, fontsize='small', markerscale=0.7)
    plt.axis('off')
    plt.savefig('shotmap{}{}.png'.format(firsthalf,secondhalf), dpi=600)
    #plt.show()
    plt.close()

    plt.figure()
    plt.axis('off')
    cbar = plt.colorbar(shots)
    cbar.set_label('Shot xG Value')
    plt.savefig('colorbar{}{}.png'.format(firsthalf,secondhalf), dpi=600)
    #plt.show()
    plt.close()

    plt.figure()
    #plt.axis('off')
    randpointsx = [1,2,3,4,5,6]
    randpointsy = [1,2,3,4,5,6]
    randpointscolor = ['orange','fuchsia','y','aqua','w','w']
    randpointslabel = ['median location','header','free kick/penalty','following dribble','other','goal','no goal']
    for i in range(len(randpointsx)):
        if i<4:
            plt.scatter(randpointsx[i],randpointsy[i],c=randpointscolor[i],marker='.')
        elif i==5:
            plt.scatter(randpointsx[i],randpointsy[i],c=randpointscolor[i],edgecolors='r',marker='o')
        else:
            plt.scatter(randpointsx[i],randpointsy[i],c=randpointscolor[i],edgecolors='#00FF00',marker='o')
    plt.plot([0,1],[0,1], alpha=0.5, ls='--', zorder=0.7, c='paleturquoise')
    plt.legend(randpointslabel)
    plt.savefig('legend{}{}.png'.format(firsthalf,secondhalf),dpi=300)
    #plt.show()
    plt.close()

    merge(firsthalf,secondhalf)


def merge(fh,sh):
    background = Image.open("shotmap{}{}.png".format(fh,sh))
    foreground = Image.open("colorbar{}{}.png".format(fh,sh))
    legend = Image.open('legend{}{}.png'.format(fh,sh))
    sblogo = Image.open('stats-bomb-logo.png')
    #3600x2400

    width,height = foreground.size
    left = 2000
    top = 325
    right = foreground.width-350
    bottom = 2600
    im1 = foreground.crop((left,top,right,bottom))
    #im1.show()
    background.paste(im1, (400,500) ,im1)

    lw,lh = legend.size
    legendleft = 250
    legendtop = 190
    legendright = legend.width-1100
    legendbottom = 700
    im2 = legend.crop((legendleft,legendtop,legendright,legendbottom))
    background.paste(im2,(800,600),im2)

    #background.paste(sblogo,(100,400),sblogo)
    #sblogo.show()
    background.show()
    background.save('shotmap{}{}.png'.format(fh,sh))


def data_range(beginning,end):
    data={}
    for i in range(beginning,end):
        xshot=[]
        yshot=[]
        xdribble = []
        ydribble = []
        with open('messishots{}{}.json'.format(i, i+1)) as f:
            shotdata = json.load(f)

        with open('messidribbles{}{}.json'.format(i,i+1)) as f:
            dribbledata = json.load(f)

        for shot in shotdata:
            xshot.append(shot['location'][0])
            yshot.append(shot['location'][1])

        for dribble in dribbledata:
            xdribble.append(dribble['location'][0])
            ydribble.append(dribble['location'][1])

        data['{}/{} Season'.format(i,i+1)] = {}
        data['{}/{} Season'.format(i,i+1)]['median shot location'] = [stat.median(xshot),stat.median(yshot)]
        data['{}/{} Season'.format(i,i+1)]['median dribble location'] = [stat.median(xdribble),stat.median(ydribble)]

        #with open('range{}{}.json'.format(beginning,end),'w') as outfile:
         #   json.dump(data,outfile)

        #with open('range{}{}.json'.format(beginning,end)) as f:
         #   newdata = json.load(f)
    #newdata= jsonify(data)
    #newdata = json.load(data)
    print(data)
    #ax = plt.figure()
    #joint_shot_chart = sns.jointplot(x='x',y='y',data = df,stat_func=None,kind='reg',space=0,color=cmap(0.1),scatter_kws={"s": 10},line_kws={'zorder':-1})
    joint_shot_chart = sns.jointplot(60, 40, data=None,stat_func=None,kind='scatter')#,scatter_kws={"s" = 0.01})
    ax=joint_shot_chart.ax_joint
    draw_pitch(ax)
    for season in data:
        print(data[season]['median shot location'])
        ax.scatter(data[season]['median shot location'][0],data[season]['median shot location'][1])
    plt.show()
        #print(season['median shot location'])
        #print(season['median shot location'][0])
        #print(type(season['median shot location'][0]))
        #plt.scatter(season['median shot location'][0],season['median shot location'][1])




#calling functions
#for i in range(2004,2019):
    #plotdribbles(i,i+1)
    #plotshots(i,i+1)
#plotdribbles(2008,2009)
plotshots(2007,2008)
data_range(2004,2006)

