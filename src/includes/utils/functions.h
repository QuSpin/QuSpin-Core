#ifndef __QUSPIN_UTILS_FUNCTIONS_H__
#define __QUSPIN_UTILS_FUNCTIONS_H__

namespace quspin {

template<typename dits_or_bits>
inline bool operator>(dits_or_bits& lhs,dits_or_bits& rhs){return lhs.content < rhs.content;}

template<typename dits_or_bits>
inline bool operator<(dits_or_bits& lhs,dits_or_bits& rhs){return lhs.content < rhs.content;}

template<typename dits_or_bits>
inline bool operator==(dits_or_bits& lhs,dits_or_bits& rhs){return lhs.content < rhs.content;}

template<typename dits_or_bits>
std::vector<int> to_vector(const dits_or_bits& s,const int length=0){
    std::vector<int> out;

    const int niter = (length>0 ? length : bit_info<typename dits_or_bits::bitset_t>::bits/s.bits)

    for(int i=0;i<niter;++i){
        out.push_back(get_sub_bitstring())
    }

}


template<typename T>
T real_value(const T v){return v;}

template<typename T>
T real_value(const std::complex<T>& v){return v.real();}

}



#endif