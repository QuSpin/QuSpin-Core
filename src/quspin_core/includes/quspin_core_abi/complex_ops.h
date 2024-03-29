#ifndef __QUSPIN_CORE_COMPLEX_OPS__
#define __QUSPIN_CORE_COMPLEX_OPS__

/*
 *  Functions to handle arithmetic operations on NumPy complex values
 */
#include <numpy/arrayobject.h>




namespace quspin_core_abi {

template <class c_type, class npy_type>
class complex_wrapper : public npy_type {

    public:
        /* Constructor */
        complex_wrapper( const c_type r = c_type(0), const c_type i = c_type(0) ){
            npy_type::real = r;
            npy_type::imag = i;
        }
        template<class _c_type,class _npy_type>
        complex_wrapper(const complex_wrapper<_c_type,_npy_type>& B){
            npy_type::real = B.real;
            npy_type::imag = B.imag;
        }
        /* Conversion */
        operator bool() const {
            if (npy_type::real == 0 && npy_type::imag == 0) {
                return false;
            } else {
                return true;
            }
        }
        operator float() const {return (float)npy_type::real;}
        operator double() const {return (double)npy_type::real;}
        operator npy_cdouble() const {return {(double)npy_type::real,(double)npy_type::imag};}
        operator npy_cfloat() const {return {(float)npy_type::real,(float)npy_type::imag};}

        /* Operators */
        complex_wrapper operator-() const {
          return complex_wrapper(-npy_type::real,-npy_type::imag);
        }
        complex_wrapper operator+(const complex_wrapper& B) const {
          return complex_wrapper(npy_type::real + B.real, npy_type::imag + B.imag);
        }
        complex_wrapper operator-(const complex_wrapper& B) const {
          return complex_wrapper(npy_type::real - B.real, npy_type::imag - B.imag);
        }
        complex_wrapper operator*(const complex_wrapper& B) const {
          return complex_wrapper(npy_type::real * B.real - npy_type::imag * B.imag, 
                                 npy_type::real * B.imag + npy_type::imag * B.real);
        }
        complex_wrapper operator/(const complex_wrapper& B) const {
          complex_wrapper result;
          c_type denom = 1.0 / (B.real * B.real + B.imag * B.imag);
          result.real = (npy_type::real * B.real + npy_type::imag * B.imag) * denom;
          result.imag = (npy_type::imag * B.real - npy_type::real * B.imag) * denom;
          return result;
        }
        /* in-place operators */
        complex_wrapper& operator+=(const complex_wrapper & B){
          npy_type::real += B.real;
          npy_type::imag += B.imag;
          return (*this);
        }
        complex_wrapper& operator-=(const complex_wrapper & B){
          npy_type::real -= B.real;
          npy_type::imag -= B.imag;
          return (*this);
        }
        complex_wrapper& operator*=(const complex_wrapper & B){
          c_type temp    = npy_type::real * B.real - npy_type::imag * B.imag;
          npy_type::imag = npy_type::real * B.imag + npy_type::imag * B.real;
          npy_type::real = temp;
          return (*this);
        }
        complex_wrapper& operator/=(const complex_wrapper & B){
          c_type denom   = 1.0 / (B.real * B.real + B.imag * B.imag);
          c_type temp    = (npy_type::real * B.real + npy_type::imag * B.imag) * denom; 
          npy_type::imag = (npy_type::imag * B.real - npy_type::real * B.imag) * denom;
          npy_type::real = temp;
          return (*this);
        }
        /* Boolean operations */
        bool operator==(const complex_wrapper& B) const{
          return npy_type::real == B.real && npy_type::imag == B.imag;
        }
        bool operator!=(const complex_wrapper& B) const{
          return npy_type::real != B.real || npy_type::imag != B.imag;
        }
        bool operator<(const complex_wrapper& B) const{
            if (npy_type::real == B.real){
                return npy_type::imag < B.imag;
            } else {
                return npy_type::real < B.real;
            }
        }
        bool operator>(const complex_wrapper& B) const{
            if (npy_type::real == B.real){
                return npy_type::imag > B.imag;
            } else {
                return npy_type::real > B.real;
            }
        }
        bool operator<=(const complex_wrapper& B) const{
            if (npy_type::real == B.real){
                return npy_type::imag <= B.imag;
            } else {
                return npy_type::real <= B.real;
            }
        }
        bool operator>=(const complex_wrapper& B) const{
            if (npy_type::real == B.real){
                return npy_type::imag >= B.imag;
            } else {
                return npy_type::real >= B.real;
            }
        }
        template <class T>
        bool operator==(const T& B) const{
          return npy_type::real == B && npy_type::imag == T(0);
        }
        template <class T>
        bool operator!=(const T& B) const{
          return npy_type::real != B || npy_type::imag != T(0);
        }
        template <class T>
        bool operator<(const T& B) const{
            if (npy_type::real == B) {
                return npy_type::imag < T(0);
            } else {
                return npy_type::real < B;
            }
        }
        template <class T>
        bool operator>(const T& B) const{
            if (npy_type::real == B) {
                return npy_type::imag > T(0);
            } else {
                return npy_type::real > B;
            }
        }
        template <class T>
        bool operator<=(const T& B) const{
            if (npy_type::real == B) {
                return npy_type::imag <= T(0);
            } else {
                return npy_type::real <= B;
            }
        }
        template <class T>
        bool operator>=(const T& B) const{
            if (npy_type::real == B) {
                return npy_type::imag >= T(0);
            } else {
                return npy_type::real >= B;
            }
        }
        template<class _c_type,class _npy_type>
        complex_wrapper& operator=(const complex_wrapper<_c_type,_npy_type>& B){
          npy_type::real = c_type(B.real);
          npy_type::imag = c_type(B.imag);
          return (*this);
        }
        template<class _c_type>
        complex_wrapper& operator=(const _c_type& B){
          npy_type::real = c_type(B);
          npy_type::imag = c_type(0);
          return (*this);
        }
};

typedef complex_wrapper<float,npy_cfloat> npy_cfloat_wrapper;
typedef complex_wrapper<double,npy_cdouble> npy_cdouble_wrapper;

template<typename ctype>
npy_cdouble_wrapper operator*(const npy_cdouble_wrapper& A, const ctype& B) {
  return npy_cdouble_wrapper(A.real * B, A.imag * B);
}
template<typename ctype>
npy_cdouble_wrapper operator*(const ctype& B, const npy_cdouble_wrapper& A) {
  return npy_cdouble_wrapper(A.real * B, A.imag * B);
}

template<typename ctype>
npy_cdouble_wrapper operator+(const npy_cdouble_wrapper& A, const ctype& B) {
  return npy_cdouble_wrapper(A.real + B, A.imag * B);
}
template<typename ctype>
npy_cdouble_wrapper operator+(const ctype& B, const npy_cdouble_wrapper& A) {
  return npy_cdouble_wrapper(A.real + B, A.imag * B);
}


npy_cdouble_wrapper operator*(const npy_cdouble_wrapper& A, const npy_cfloat_wrapper& B) {
  return npy_cdouble_wrapper(A.real * B.real - A.imag * B.imag, 
                             A.real * B.imag + A.imag * B.real);
}
npy_cdouble_wrapper operator*(const npy_cfloat_wrapper& A, const npy_cdouble_wrapper& B) {
  return npy_cdouble_wrapper(A.real * B.real - A.imag * B.imag, 
                             A.real * B.imag + A.imag * B.real);
}

npy_cdouble_wrapper operator*(const npy_cfloat_wrapper& A, const double& B) {
  return npy_cdouble_wrapper(A.real * B, A.imag * B);
}
npy_cdouble_wrapper operator*(const double& B, const npy_cfloat_wrapper& A) {
  return npy_cdouble_wrapper(A.real * B, A.imag * B);
}
npy_cfloat_wrapper operator*(const npy_cfloat_wrapper& A, const float& B) {
  return npy_cfloat_wrapper(A.real * B, A.imag * B);
}
npy_cfloat_wrapper operator*(const float& B, const npy_cfloat_wrapper& A) {
  return npy_cfloat_wrapper(A.real * B, A.imag * B);
}

npy_cdouble_wrapper operator+(const npy_cdouble_wrapper& A, const npy_cfloat_wrapper& B) {
  return npy_cdouble_wrapper(A.real + B.real, A.imag + B.imag);
}
npy_cdouble_wrapper operator+(const npy_cfloat_wrapper& A, const npy_cdouble_wrapper& B) {
  return npy_cdouble_wrapper(A.real + B.real, A.imag + B.real);
}
npy_cdouble_wrapper operator+(const npy_cfloat_wrapper& A, const double& B) {
  return npy_cdouble_wrapper(A.real + B, A.imag);
}
npy_cdouble_wrapper operator+(const double& B, const npy_cfloat_wrapper& A) {
  return npy_cdouble_wrapper(A.real + B, A.imag);
}
npy_cfloat_wrapper operator+(const npy_cfloat_wrapper& A, const float& B) {
  return npy_cfloat_wrapper(A.real + B, A.imag);
}
npy_cfloat_wrapper operator+(const float& B, const npy_cfloat_wrapper& A) {
  return npy_cfloat_wrapper(A.real + B, A.imag);
}




inline npy_cdouble_wrapper conj(const npy_cdouble_wrapper& A) {
  return npy_cdouble_wrapper(A.real, -A.imag);
}

inline npy_cfloat_wrapper conj(const npy_cfloat_wrapper& A) {
  return npy_cfloat_wrapper(A.real, -A.imag);
}

inline double conj(const double& A) {return A;}

inline float conj(const float& A) {return A;}

inline npy_int16 conj(const npy_int16& A) {return A;}

inline npy_int8 conj(const npy_int8& A) {return A;}

inline double real(const npy_cdouble_wrapper& A) {return A.real;}

inline float real(const npy_cfloat_wrapper& A) {return A.real;}

inline double real(const double& A) {return A;}

inline float real(const float& A) {return A;}

inline npy_int16 real(const npy_int16& A) {return A;}

inline npy_int8 real(const npy_int8& A) {return A;}

inline double imag(const npy_cdouble_wrapper& A) {return A.imag;}

inline float imag(const npy_cfloat_wrapper& A) {return A.imag;}

inline double imag(const double& A) {return 0;}

inline float imag(const float& A) {return 0;}

inline npy_int16 imag(const npy_int16& A) {return 0;}

inline npy_int8 imag(const npy_int8& A) {return 0;}

}


namespace quspin {
    using namespace quspin_core_abi; // insert these definitions into quspin namespace
}

#include <quspin/quspin.h>


#endif