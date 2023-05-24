import numpy as np

from datetime import datetime, timedelta
from collections import defaultdict
import uuid


FIELDS = {
  'wifi': {
    'range' : [1, 3601],
    'type' : 'int',
  },
    
  'app': {
    'range' : [0, 2],
    'type' : 'int'
  },
  'instagram_time': {
    'range' : [1, 3601],
    'type' : 'int'
  },
  'facebook_time': {
    'range' : [1, 3601],
    'type' : 'int'
  },
  'snapchat_time': {
    'range' : [1, 3601],
    'type' : 'int'
  },
  'quiz_time': {
    'range' : [1, 3601],
    'type' : 'int'
  },
  'class_material': {
    'range' : [0, 2],
    'type' : 'int'
  },
  'nivel_baterie': {
    'range' : [0, 1],
    'type' : 'float'
  },
  'app_noua': {
    'range' : [0, 2],
    'type' : 'int'
  },
}

CORRELATIONS = [
  {
   'fields' : ['instagram_time', 'facebook_time', 'quiz_time', 'quiz_time'],
   'maxval' : 3600,
  },
  
]

def random_walk_next(prev, val_type, val_min, val_max, fraction=0.1, reset_proba=0.25):
  step_min = val_min
  step_max = val_max * fraction
  if val_type == 'int':
    func = np.random.randint
    step_max = int(step_max) + 1
  else:
    func = np.random.uniform  
  if prev is None or np.random.randint(0,100) <= reset_proba: # if first or reset
    prev = func(val_min, val_max)  
  direction = 1 if np.random.randint(0,100) >=50 else -1
  step = func(step_min, step_max)
  increment = direction * step
  val = np.clip(prev + increment, val_min, val_max) 
  if val_type == 'int':
    val = int(val)
  return val


def get_user_data(start_date='2023-01-01', 
                  start_hour='10:00:00', 
                  end_hour='17:00:00',
                  n_obs=100):
  data_config = FIELDS
  result = defaultdict(list)
  start = start_date + ' ' + start_hour
  end_day_one = start_date + ' ' + end_hour
  start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
  current_end_hour = datetime.strptime(end_day_one, '%Y-%m-%d %H:%M:%S').hour
  current_date = start_date
  day_cnt = 1
  all_fields = list(data_config.keys())
  for cnt in range(n_obs):
    time = current_date.strftime('%Y-%m-%d %H:%M:%S')
    result['time'].append(time)
    # generate values
    for fld in all_fields:
      val_type = data_config[fld]['type']
      val_min, val_max = data_config[fld]['range']
      prev = data_config[fld].get('value')
      val = random_walk_next(prev, val_type, val_min, val_max)
      data_config[fld]['value'] = val
      result[fld].append(round(val,2))
      prev = val
    # increment time
    if current_date.hour >= current_end_hour:
      current_date = start_date + timedelta(hours=24 * day_cnt)
      current_date = current_date.replace(hour=np.random.choice(range(9,12)))
      day_cnt += 1
      current_end_hour = np.random.choice(range(14,22)) # reset end-screen-time hour
      for fld in all_fields:
        data_config[fld]['value'] = None # reset new day
    else:
      current_date += timedelta(hours=1)
    # check data correlations
    for dct_corr in CORRELATIONS:
      fields = dct_corr['fields']
      maxval = np.random.randint(dct_corr['maxval'] // 2, dct_corr['maxval'])
      # no exp - positive values
      vals_exp = [result[x][-1] for x in fields]
      sum_exp = np.sum(vals_exp)
      old_vals = {x:result[x][-1] for x in fields}
      for fld in fields:
        prc = old_vals[fld] / sum_exp
        result[fld][-1] = round(prc * maxval,2) if data_config[fld]['type'] != 'int' else int(prc * maxval)
      #endfor
    #endfor
  return result
    
    
def get_data(start_date='2023-01-01', 
             start_hour='10:00:00', 
             end_hour='17:00:00',
             n_obs=100, 
             n_users=2, 
             reset=False):
  result = []
  for usr in range(n_users):
    uid = str(uuid.uuid4())[:8]
    data = get_user_data(
      start_date=start_date, 
      start_hour=start_hour, 
      end_hour=end_hour,
      n_obs=n_obs
    )
    result.append({
      'id' : uid,
      'reset' : reset,
      'data' : data
    })
  return result
    

if __name__ == '__main__':
  import pandas as pd
  pd.set_option('display.max_columns', 500)
  pd.set_option('display.width', 1000)
  pd.set_option('display.max_rows', 200)  
  all_data = get_data()
  df = pd.DataFrame(all_data[0]['data'])
  print(df)