# assignment operators
# binary operators
# transposition
A = [ 1, 2, 3;
       4, 5, 6;
       7, 8, 9 ] ;
B = A;
C = A;     # assignemnt with unary expression
print C;
C = B' ;    # assignemnt with matrix transpose
print C;
C = A+B ;   # assignemnt with binary addition
print C;
C = A-B ;   # assignemnt with binary substraction
print C;
C = A*B ;   # assignemnt with binary multiplication
print C;
C = A/B ;   # assignemnt with binary division
print C;
C = A.+B ;  # add element-wise A to B
print C;
C = A.-B ;  # substract B from A
print C;
C = A.*B ;  # multiply element-wise A with B
print C;
C = A./B ;  # divide element-wise A by B
print C;

C += B ;  # add B to C
print C;
C -= B ;  # substract B from C
print C;
C *= A ;  # multiply A with C
print C;
C /= A ;  # divide A by C
print C;



