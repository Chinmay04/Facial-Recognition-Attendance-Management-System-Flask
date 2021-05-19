import mysql.connector
import pandas as pd
import datetime

class Fetcher():
    def __init__(self, username):
        self.username = username
        self.connDb = mysql.connector.connect(host='localhost', user='root', password='dptstillworking', database=self.username)
        self.cDb = self.connDb.cursor()

    def fetch_names(self):
        self.name_query = 'select name from members'
        self.cDb.execute(self.name_query)
        self.names = self.cDb.fetchall()
        self.all_names = [self.i[0] for self.i in self.names]
        print('NAM',self.all_names)
        return self.all_names

    def fetch_sessions(self):
        self.name_query = 'select name from sessions'
        self.cDb.execute(self.name_query)
        self.names = self.cDb.fetchall()
        self.all_sessions = [self.i[0] for self.i in self.names]
        return self.all_sessions

    def fetch_dates(self):
        self.name_query = 'select distinct date from attendance'
        self.cDb.execute(self.name_query)
        self.names = self.cDb.fetchall()
        self.all_dates = [self.i[0] for self.i in self.names]
        return self.all_dates

    def fetch_attendance(self):
    	self.name_query = 'select * from attendance'
    	self.cDb.execute(self.name_query)
    	self.all_record = self.cDb.fetchall()
    	return self.all_record

    def fetch_filtered_record(self, filters):
        self.percent = -1
        self.all_session_percents = []
        
        if filters['dates']!='Date' and filters['sessions']=='Session' and filters['members']=='Member':
            self.query = f"select * from attendance where date = '{filters['dates']}'"
            self.header = ('ID', 'Session','Date', 'Time') + tuple(self.fetch_names())

        elif filters['dates']=='Date' and filters['sessions']!='Session' and filters['members']=='Member':
            self.query = f"select * from attendance where session = '{filters['sessions']}'"
            self.header = ('ID', 'Session','Date', 'Time') + tuple(self.fetch_names())

        elif filters['dates']=='Date' and filters['sessions']=='Session' and filters['members']!='Member':
            self.query = f"select id,session,date,time,{filters['members']} from attendance"

            self.header = ('ID', 'Session','Date', 'Time', filters['members'])
            self.record_query = f"select {filters['members']} from attendance"
            self.tcDb = self.connDb.cursor()
            self.tcDb.execute(self.record_query)
            self.values = [self.i[0] for self.i in self.tcDb.fetchall()]
            self.percent = self.values.count(1)/len(self.values)*100
            self.all_session_percents = {}

            for i in self.fetch_sessions():
                self.record_query = f"select {filters['members']} from attendance where session='{i}'"
                self.tcDb.execute(self.record_query)
                self.current_values = [self.i[0] for self.i in self.tcDb.fetchall()]
                if self.current_values == []:
                    self.sub_percent = 0
                else:
                    self.sub_percent = self.current_values.count(1)/len(self.current_values)*100
                self.all_session_percents[i] = self.sub_percent

        elif filters['dates']!='Date' and filters['sessions']!='Session' and filters['members']=='Member':
            self.query = f"select * from attendance where session = '{filters['sessions']}' and date = '{filters['dates']}'"
            self.header = ('ID', 'Session','Date', 'Time') + tuple(self.fetch_names())

        elif filters['dates']=='Date' and filters['sessions']!='Session' and filters['members']!='Member':
            self.query = f"select id,session,date,time,{filters['members']} from attendance where session = '{filters['sessions']}'"
            self.header = ('ID', 'Session','Date', 'Time', filters['members'])

        elif filters['dates']!='Date' and filters['sessions']!='Session' and filters['members']!='Member':
            self.query = f"select id,session,date,time,{filters['members']} from attendance where session = '{filters['sessions']}' and date = '{filters['dates']}'"        
            self.header = ('ID', 'Session','Date', 'Time',filters['members'])

        elif filters['dates']!='Date' and filters['sessions']=='Session' and filters['members']!='Member':
            self.query = f"select id,session,date,time,{filters['members']} from attendance where date = '{filters['dates']}'"        
            self.header = ('ID', 'Session','Date', 'Time',filters['members'])

        else:
            self.query = 'select * from attendance'
            self.header = ('ID', 'Session','Date', 'Time') + tuple(self.fetch_names())

        self.cDb.execute(self.query)
        self.result = self.cDb.fetchall()
        self.result.insert(0, self.header)
  
        return self.result, self.header, self.percent, self.all_session_percents

    def fetch_member_record(self, name):
        self.cDb.execute(f"select id,name,rollno,email,contact,path from members where name='{name}'")
        self.result = list(self.cDb.fetchall()[0])

        return self.result

    def fetch_all_members(self):
        self.cDb.execute(f"select id,name,rollno,email,contact,path from members")
        self.result = self.cDb.fetchall()
        print(self.result)
        return self.result

    def fetch_records_file(self):
        self.file_query = 'select * from attendance'
        self.file = pd.read_sql_query(self.file_query, self.connDb)
        self.file.to_csv('static/User Accounts/'+self.username+'/sheets/records.csv')


    def fetch_percent_sessions(self):
        #Fetches average attendance of all members in each session
        self.all_session_percentage={}
        
        for self.s in self.fetch_sessions():
            # print(self.s)
            print('NNNSSS',self.fetch_sessions(),self.fetch_names())
            if self.fetch_sessions() ==[] or self.fetch_names() ==[]:
                return self.all_session_percentage
            self.query = f'select {self.fetch_names()} from attendance'.replace('[','').replace(']','').replace("'","`")
            self.query = self.query + f" where session='{self.s}'"
            self.cDb.execute(self.query)
            self.curr_values = self.cDb.fetchall()
            self.no_of_members = len(self.fetch_names())
            self.curr_per_values = []
            if self.curr_values == []:
                print('HEREEEE')
                self.all_session_percentage[self.s] = 0
            else:
                print(self.s)
                for self.i in self.curr_values:
                    self.curr_per_values.append((self.i.count(1)/self.no_of_members)*100)
                self.all_session_percentage[self.s] = sum(self.curr_per_values)/len(self.curr_per_values)

        return self.all_session_percentage

    def fetch_today_percent_sessions(self):
        self.all_session_percentage={}
        print('NNNSSS',self.fetch_sessions(),self.fetch_names())
        if self.fetch_sessions() ==[] or self.fetch_names() ==[]:
            return self.all_session_percentage
        self.date=datetime.datetime.now().strftime('%Y-%m-%d')#'2021-04-25'
        # self.d='2021-04-01'
        self.q= f"select session from attendance where date='{self.date}'"
        self.cDb.execute(self.q)
        self.todays_sessions = [self.i[0] for self.i in self.cDb.fetchall()]
        for self.s in self.todays_sessions:
            self.query = f'select {self.fetch_names()} from attendance'.replace('[','').replace(']','').replace("'","`")
            self.query = self.query + f" where session='{self.s}' and date='{self.date}'"
            self.cDb.execute(self.query)
            self.curr_values = self.cDb.fetchall()
            self.no_of_members = len(self.fetch_names())
            self.curr_per_values = []
            for self.i in self.curr_values:
                print(self.i.count(1))
                self.curr_per_values.append((self.i.count(1)/self.no_of_members)*100)
            self.all_session_percentage[self.s] = sum(self.curr_per_values)/len(self.curr_per_values)
        return self.all_session_percentage

    def fetch_member_session_percent(self, memname):
        #Fetches average attendance of a member in each session
        self.all_session_percents = {}
        if self.fetch_sessions() ==[] or self.fetch_names() ==[]:
            return self.all_session_percents
        self.record_query = f"select `{memname}` from attendance"
        self.tcDb = self.connDb.cursor()
        self.tcDb.execute(self.record_query)

        self.values = [self.i[0] for self.i in self.tcDb.fetchall()]
        if self.values == []:
            self.percent = 0
            for i in self.fetch_sessions():
                self.all_session_percents[i] = 0
        else:
            self.percent = self.values.count(1)/len(self.values)*100
            print(self.fetch_sessions())
            for i in self.fetch_sessions():
                self.record_query = f"select `{memname}` from attendance where session='{i}'"
                self.tcDb.execute(self.record_query)
                self.current_values = [self.i[0] for self.i in self.tcDb.fetchall()]
                if self.current_values == []:
                    self.all_session_percents[i] = 0
                else:
                    self.sub_percent = self.current_values.count(1)/len(self.current_values)*100
                    self.all_session_percents[i] = self.sub_percent
        
        return self.percent, self.all_session_percents

    def fetch_avg_attendance_all_members(self):
        #fetches overall average attendance of all members
        self.avg_all_members = []
        if self.fetch_sessions() ==[] or self.fetch_names() ==[]:
            return self.avg_all_members
        for self.i in self.fetch_names():
            self.record_query = f"select `{self.i}` from attendance"
            self.tcDb = self.connDb.cursor()
            self.tcDb.execute(self.record_query)
            self.res = self.tcDb.fetchall()
            print('SSSS',self.res)
            if self.res ==[]:
                self.avg_all_members.append(0)
            else:
                self.values = [self.i[0] for self.i in self.res]
                self.percent = self.values.count(1)/len(self.values)*100
                self.avg_all_members.append(round(self.percent,2))

        return self.avg_all_members

    def deleteMember(self, memid, name):
        print(memid,name)
        self.mem_query = f"alter table attendance drop column {name}"
        self.att_query = f"delete from members where id={memid}"
        self.tcDb = self.connDb.cursor()
        self.tcDb.execute(self.mem_query)
        self.tcDb.execute(self.att_query)
        self.connDb.commit()
        print('Deleted')
    
    def fetch_present_absent(self, details, memname):
        print(details, memname)   
        self.paquery = f"select {memname} from attendance where date='{details[0]}' and time='{details[1]}' and session='{details[2]}'"
        self.tcDb = self.connDb.cursor()
        self.tcDb.execute(self.paquery)  
        return self.tcDb.fetchall()[0][0]

    def fetch_edit_records(self):
        self.query = f"select date, time, session from attendance"
        self.tcDb = self.connDb.cursor()
        self.tcDb.execute(self.query)
        self.edrecs = [i[0]+' '+i[1]+' '+i[2] for i in self.tcDb.fetchall()]
        self.n = self.fetch_names()
        print(self.edrecs)
        print(self.n)
        return self.edrecs, self.n

    def update_record(self, details, memname, r):
        if int(r)==0:
            self.upquery = f"update attendance set {memname}=1 where date='{details[0]}' and time='{details[1]}' and session='{details[2]}'"
        else:
            self.upquery = f"update attendance set {memname}=0 where date='{details[0]}' and time='{details[1]}' and session='{details[2]}'"
        print(self.upquery)
        self.tcDb = self.connDb.cursor()
        self.tcDb.execute(self.upquery)
        self.connDb.commit()
        print('Updated')
