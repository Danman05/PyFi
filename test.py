from Ticker import Ticker
import time

t_start = time.time()



ticker = Ticker('FFIE')


t_end = time.time()

# print([i for i in dir(ticker) if not i.startswith('__')])
print(vars(ticker))
time_elapsed = t_end - t_start

print(f'Created ticker - time elapsed {time_elapsed}')

