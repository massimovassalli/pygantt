import numpy as np

def setValue(val,ar,default):
    if val in ar:
        return ar[val]
    else:
        return default
    
class deliverable(object):
    def __init__(self,deli,defaults,task) -> None:
        self.month = deli['month']
        self.id = deli['id']
        self.color = setValue('color',deli,task.color)
        self.font_size = setValue('font_size',deli,defaults['font_size_labels'])

class task(object):
    def __init__(self,tdata,defaults) -> None:
        self._deliverables = []
        self.start = setValue('start',tdata,0)
        self.stop = setValue('stop',tdata,1)
        self.id = tdata['id']
        self.title = tdata['title']
        self.color = setValue('color',tdata,defaults['task_color'])
        self.id_color = setValue('id_color',tdata,self.color)
        self.title_color = setValue('title_color',tdata,self.color)
        
        if 'deliverables' in tdata:
            for deli in tdata['deliverables']:
                self._deliverables.append(deliverable(deli,defaults,self))

class workpackage(object):

    def __init__(self,wps,defaults) -> None:
        self._tasks=[]
        self.id = wps['id']
        self.title = wps['title']
        self.color = setValue('color',wps,defaults['wp_color'])
        self.id_color = setValue('id_color',wps,self.color)
        self.title_color = setValue('title_color',wps,self.color)
            
        if 'tasks' in wps:
            for tdata in wps['tasks']:
                self._tasks.append(task(tdata,defaults))

    
    @property
    def start(self):
        st=[]
        for t in self._tasks:
            st.append(t.start)
        return min(st)
    
    @property
    def stop(self):
        st=[]
        for t in self._tasks:
            st.append(t.stop)
        return max(st)    
        
class dataset(object):
    def __init__(self,data,defaults) -> None:
        self.id = data['id']
        self.color = setValue('color',data,defaults['set_color'])
        self.id_color = setValue('id_color',data,self.color)
        self.text_color = setValue('text_color',data,defaults['text_color'])
        self.labels = setValue('labels',data,None)
        self.symbol = setValue('symbol',data,'o')
        self.font_size = setValue('font_size',data,defaults['font_size_labels'])
        self.size = setValue('size',data,5)
        self.data = self.setTicks(data['data'])        
    
    def setTicks(self,data):
        if 'start' in data:
            start = float(data['start'])
            stop = float(data['stop'])
            if 'step' in data:
                step = float(data['step'])
            else:
                step = 1
            return np.arange(start,stop,step)
        else:
            return data      

class gantt(object):    
        
    def __init__(self,all) -> None:
        self._wps=[]
        self._sets=[]
        self.id = setValue('id',all,'ID')
        self.title = setValue('title',all,'Title')
        self.cstyle = setValue('colorstyle',all,None)
        self.aspectratio = (11.69,8.27)
        if 'aspectratio' in all:
            if all['aspectratio'] == "A4":
                self.aspectration = (11.69,8.27)
            elif all['aspectratio'] == "4:3":
                self.aspectration = (12,9)
            elif all['aspectratio'] == "16:9":
                self.aspectration = (12,6.75)

        self.scalefactor = float(setValue('scalefactor',all,1.0))
        self.fontsize = int(setValue('fontsize',all,10))
        
        self.defaults = {'wp_color':'b','task_color':'g','set_color':'b','text_color':'w',
                         'font_size':10,'font_size_labels':8}
        for key in self.defaults:
            self.defaults[key] = setValue(key,all,self.defaults[key])
        
        if 'WP' in all:
            for wp in all['WP']:
                self._wps.append(workpackage(wp,self.defaults))
        
        if 'sets' in all:
            for st in all['sets']:
                self._sets.append(dataset(st,self.defaults))        

    @property
    def nmonths(self):
        st = []
        for t in self._wps:
            st.append(t.stop)
        return max(st)