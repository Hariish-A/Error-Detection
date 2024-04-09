def validate_input(data, bits= None):
  if not all([(x=='0' or x=='1') for x in data]):
    raise ValueError('Entered data is not in binary')
  if bits and (len(data)!=bits):
    raise ValueError('Number of bits and size of entered data do not match')

def make_parity(data, par) :
  if par not in ['o','e']:
    raise ValueError('Invalid value entered for parity.')
  if par == 'o':
    data = (data+'1') if data.count('1')%2==0 else (data+'0')
  else:
    data = (data+'1') if data.count('1')%2==1 else (data + '0')

  return data

def check_parity(data, par):
  if par=='o':
    return data.count('1')%2 ==1
  else:
    return data.count('1')%2 ==0

def simple_parity_check():
  bits = int(input("Enter number of bits :"))
  par = input('Enter o for odd parity and e for even parity :').lower()
  data = input("Enter data to be transmitted :")

  validate_input(data, bits)

  data = make_parity(data,par)

  print('Transmitted data with parity :', data)

  rx_data = input('Enter recieved data :')

  validate_input(rx_data, bits+1)

  if check_parity(rx_data, par):
    print('Data is recieved without noise.')
  else:
    print('There is noise in the recieved data.')

def two_dimensional_parity_check():
  bits = int(input("Enter number of bits :"))
  count = int(input("Enter the number of data items:"))
  par = input('Enter o for odd parity and e for even parity :').lower()
  data = []

  for i in range(count):
    a = input('Enter the data :')
    validate_input(a, bits)
    data.append(a)

  for i in range(count):
    data[i] = make_parity(data[i],par)

  last = ''
  s = ''

  for i in range(bits):
    for j in range(count):
      s += data[j][i]
    if par == 'o':
      last = (last +'1') if s.count('1')%2==0 else (last +'0')
    else:
      last = (last+'1') if s.count('1')%2==1 else (last + '0')
    s = ''
  data.append(make_parity(last,par))
  print(data)

  rx_data = []
  for i in range(len(data)):
    a = input('Enter recieved data :')
    validate_input(a,bits+1)
    rx_data.append(a)
  changed = False
  s = ''
  for i in range(count):
    if not check_parity(rx_data[i],par):
      changed = True
      for k in range(bits):
        s = ''
        for j in range(count+1):
          s += rx_data[j][k]
        if not check_parity(s,par):
            print(f'The bit number {k+1} in data item {1+i} is changed.')
            break
  if not changed:
    print('No noise in data detected.')

def divide(data, divisor):
  # data += '0'* ( len(divisor) - 1)
  left_data = data
  rem = ''
  for i in range(len(data) - len(divisor)+1):
    content = left_data[:len(divisor)]
    # print(f'{content=} {left_data}')
    if content[0] == '1':
      rem = bin(int(content,2) ^ int(divisor,2))[2:]
      rem = '0'* (len(divisor) -len(rem)) + rem
      rem = rem[1:]
      # print(rem)
    else:
      rem = bin(int(content,2) ^ 0)[2:]
      rem = '0'* (len(divisor) -len(rem)) + rem
      rem = rem[1:]
      # print(rem)
    if (len(divisor)+i) == len(data):
      left_data = rem + data[-1]
      break
    else:
      left_data = rem + data[len(divisor)+i]
  return rem

def cyclic_redundancy_check():
  inp_data = input("Enter the data :")
  validate_input(inp_data)

  divisor = input("Enter the divisor :")
  validate_input(divisor)

  data = inp_data + ('0'* ( len(divisor) - 1) )

  print('Transmitted data :', inp_data + divide(data, divisor))

  rx_data = input("Enter recieved data : ")
  validate_input(rx_data)

  if len(rx_data) != ( len(inp_data) + len(divisor) -1 ):
    raise ValueError('Number of bits and size of entered data do not match')


  if int(divide(rx_data, divisor),2) != 0:
    print('There is noise in the data.')
  else:
    print('No noise in data detected.')

def find_checksum(data, k):
  size = len(data) // k
  dataset = [data[i*size:((i*size)+size)] for i in range(k)]


  while(len(dataset) != 1):
    temp = bin(int(dataset[0],2) + int(dataset[1],2))
    if len(temp[2:]) > size:
      temp = bin (int( temp[(2+len(temp[2:])-size) :], 2) + 1)[2:]
    elif len(temp[2:]) == size:
      temp = temp[2:]
    else:
      temp = temp[2:]
      temp = '0'*(size-len(temp)) + temp
    dataset[0] = temp
    del dataset[1]
  inv = ''
  for i in dataset[0]:
    if i=='0':
      inv +='1'
    else:
      inv +='0'

  return inv

def checksum():
  # data , k= '1111111111010001',2
  data = input('Enter data :')
  validate_input(data)
  k = int(input("Enter value of k :"))

  print('Transmitted data = ', data+ find_checksum(data,k))

  rx_data = input('Enter recieved data : ')
  validate_input(rx_data)
  k+=1

  inv = find_checksum(rx_data,k)
  if int(inv,2) == 0:
    print('No error detected.')
  else:
    print('Error detected! Recieved checksum answer is ', inv)

print('1. Simple parity check. \n2. 2 Dimensional Parity Check. \n3. Cyclic Redundancy Check \n4. Checksum')
choice = int(input('Enter your choice :'))

match choice:
  case 1:
    simple_parity_check()
  case 2:
    two_dimensional_parity_check()
  case 3:
    cyclic_redundancy_check()
  case 4:
    checksum()
  case _:
    raise ValueError('Invalid choice entered.')