import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from lifelines import KaplanMeierFitter

# Read csv file and make dataframe
liver_patient = pd.read_csv('cirrhosis.csv')
patient_df = pd.DataFrame(liver_patient)

# Checking how much unknown values we have in Stage 

our_patients = patient_df[['N_Days','Status','Age','Sex','Stage']]
missing_values = our_patients.isnull().sum().sum()
all_values = our_patients.count().sum()
percent = (missing_values/all_values)*100

if percent <10:
    print("Number of missing values is less than 10%.")

    # Age is presented in days and for this reason we treat is as continuous variable

    # Creating a histogram of age
    age = patient_df['Age']
    plt.hist(age, bins=10, color = '#03A64A', alpha=0.5, edgecolor='black')
    plt.title('Histogram of Age')
    plt.xlabel('Age [days]')
    plt.ylabel('Frequency of Occurance')
    plt.autoscale()
    plt.grid()
    plt.show()

    # Creating a pie chart of Sex
    female=len(patient_df[patient_df['Sex'] == 'F'])
    male=len(patient_df[patient_df['Sex'] == 'M'])

    sex_labels = ['Male','Female']

    plt.pie([male,female], labels = sex_labels, autopct='%0.2f', pctdistance=0.7, explode=[0.1,0], colors=['#6A5ACD','#DA70D6'])
    plt.title('Pie chart of sex of patients')
    plt.show()

    # Creating a pie plot of stage of cirrhosis

    if 'Stage' in our_patients.columns:
        stage = our_patients['Stage'].fillna('Unknown')

        stage_counts = stage.value_counts()

        if not stage_counts.empty:
            stage_labels = ['Stage 3', 'Stage 4', 'Stage 2', 'Stage 1', 'No Data']
            plt.pie(stage_counts, labels=stage_labels, autopct='%0.2f', pctdistance=0.7, explode=[0.1,0,0,0,0.2],
                    colors=['#35403A', '#4D5950', '#A3A69C', '#BFBFB8', '#BABF95'])
            plt.title('Pie chart of stage of cirrhosis')
            plt.show()
        else:
            print("No valid data for the 'Stage' column.")
    else:
        print("The 'Stage' column does not exist in the DataFrame.")


    # Creating a histogram of days between registration and the earlier of death,
    # transplantation, or study analysis time in July 1986

    N_days = patient_df['N_Days']

    plt.hist(N_days, color = '#DC143C', edgecolor='black')
    plt.title(f'Histogram of days between registration and the earlier of death, \ntransplantation, 
              or study analysis time in July 1986 and status of the patient')
    plt.xlabel('Number of days')
    plt.ylabel('Frequency of Occurance')
    plt.autoscale()
    plt.grid()
    plt.show()

    # Creating a pie chart of status of the patient C (censored), CL (censored due to liver tx), or D (death)
    status = patient_df['Status']
    C=len(status[status == 'C'])
    CL=len(status[status == 'CL'])
    D=len(status[status == 'D'])
    status_list = [C,CL,D]

    status_labels = ['Censored','Censored due to liver tx','Death']

    plt.pie([C, CL, D], autopct='%0.2f', pctdistance=0.7, colors=['#F08080', '#FF4500', '#FFD700'], explode=[0.1,0,0]) 
    plt.title('Pie chart of the Status of Patients')
    plt.legend(status_labels, loc=5)
    plt.show()

# Descriptive statistics function
    def stat (data):
        des = data.describe()
        print(des,'\nSkewness = ', stats.skew(data),'\nKurtosis = ', stats.kurtosis(data))

    print(5*'*','Statistics for number of days in hospitalization', 5*'*')
    print(stat(N_days))
    print(5*'*','Statistics for age', 5*'*')
    print(stat(age))
    
# Box plot for categorical valiable 'Status' and continous variable 'N_Days'
    cens = our_patients.loc[our_patients['Status']== 'C']
    cons_liver = our_patients.loc[our_patients['Status']== 'CL']
    death = our_patients.loc[our_patients['Status']== 'D']
    
    plt.subplot(131)
    plt.boxplot(cens['N_Days'])
    plt.title('N_Days for Censored')

    plt.subplot(132)
    plt.boxplot(cons_liver['N_Days'])
    plt.title('N_Days for censored liver')

    plt.subplot(133)
    plt.boxplot(death['N_Days'])
    plt.title('N_Days for dead')
    plt.tight_layout()
    plt.show()

# Survival analysis plot
    
    n_df = our_patients.loc[:,['Status','N_Days']]
    new_df = n_df.replace('D', 0).replace(['C', 'CL'], 1)
    

    kmf = KaplanMeierFitter() 
    X= new_df['N_Days']
    Y = new_df['Status']
    kmf.fit(X, Y) 
    kmf.plot(color = '#FFB300') 
    plt.title('Estimations of Kaplan Meier') 
    plt.xlabel('Number of Days After Hospital Admission') 
    plt.ylabel('Survival')
    plt.show()
    
else:
    print("Number of missing values is greater then 10%.")