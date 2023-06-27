from multiprocessing import Pool, cpu_count
from time import time
import logging


def factorize(*number):
	all_list = list()
	for el in number:
		num = int(1)
		num_list = list()
		for i in range(num, el+1):
			if not el % i:
				num_list.append(i)
		all_list.append(num_list)
	#print(all_list)
	return all_list


def callback(result):
	print(
		f'a_cpu*{cpu_count()}-core = {result[0]}\n'
		f'b_cpu*{cpu_count()}-core = {result[1]}\n'
		f'c_cpu*{cpu_count()}-core = {result[2]}\n'
		f'd_cpu*{cpu_count()}-core = {result[3]}'
		)


if __name__ == '__main__':
	timer1 = time()
	a, b, c, d  = factorize(128, 255, 99999, 10651060)
	print(
	f'a = {a}\n'
	f'b = {b}\n'
	f'c = {c}\n'
	f'd = {d}'
	)
	print(f'One process time: {round(time() - timer1, 4)}s\n')
	print(f"Count CPU: {cpu_count()}")
	timer2 = time()
	with Pool(cpu_count()) as p:
		p.map_async(
			factorize,
			(128, 255, 99999, 10651060),
			callback=callback,
			)
		p.close()
		p.join()
	print(f'Done by {cpu_count()} processes: {round(time() - timer2, 4)}')


#assert a == [1, 2, 4, 8, 16, 32, 64, 128]
#assert b == [1, 3, 5, 15, 17, 51, 85, 255]
#assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
#assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]
