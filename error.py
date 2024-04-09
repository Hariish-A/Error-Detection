def check_parity(rx_data,parity):
  if parity == "e":
    if rx_data.count('1') % 2 == 0:
      return True
    else:
      return False
  else:
    if rx_data.count('1') % 2 == 1:
      return True
    else:
      return False
    
def simple_parity():
  bits = int(input("Enter the number of bits : "))
  parity = input("Enter o for odd parity and e for even parity : ")
  data = input("Enter the data : ")
  data = set_parity(data,parity)
  print("Transmitted data : ",data)

  rx_data = input('Enter recieved data :')

  flag = check_parity(rx_data,parity)

  if flag == True:
    print("The Data is transmitted without any error.")
  else:
    print("The Transmitted data has an error.")

def set_parity(data,parity):
  if parity == 'o':
    data = (data+'1') if data.count('1')%2==0 else (data+'0')
  else:
    data = (data+'1') if data.count('1')%2==1 else (data + '0')
  return data

def two_dim_parity():
  bits = int(input("Enter the number of bits : "))
  count = int(input("Enter number of data sets : "))
  parity = input("Enter o for odd parity and e for even parity : ").lower()
  result = []
  for i in range(count):
    a = input("Enter the data : ")
    a = set_parity(a,parity)
    result.append(a)

  s = ''
  last = ''

  for i in range(bits):
    for j in range(count):
      s += result[j][i]
    if parity == 'o':
      last = (last+'1') if s.count('1')%2==0 else (last+'0')
    else:
      last = (last+'1') if s.count('1')%2==1 else (last+'0')

    s = ''
  last = set_parity(last,parity)
  result.append(last)
  print("Transmitted data : ",result)

  rx_data = []
  for i in range(len(result)):
    a = input("Enter received data : ")
    rx_data.append(a)

  changed = False
  s = ''

  for i in range(count):
    if not check_parity(rx_data[i],parity):
      changed = True
      for j in range(bits):
        s = ''
        for k in range(count + 1):
          s += rx_data[k][j]
        if not check_parity(s,parity):
          print(f'The bit number {j+1} in data item {1+i} is changed.')
          break
  if not changed:
    print("No error in data.")

def main():
  print("1.Simple Parity Check")
  print("2.Two Dimensional Parity Check")
  choice = int(input("Enter your choice : "))
  match choice:
    case 1:
      simple_parity()
    case 2:
      two_dim_parity()

if __name__ == "__main__":
  main()