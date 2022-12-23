#ifndef __QUSPIN_BASIS_TYPES_H__
#define __QUSPIN_BASIS_TYPES_H__

#include "basis/basis.h"
#include "basis/symmetry.h"
#include "matrix/operator.h"

namespace quspin {

template<typename I,typename T>
using dit_symmetry = basis::symmetry<basis::dit_perm<I>, basis::perm_dit<I>, basis::bitbasis::dit_set<I>,T>;

template<typename I,typename J,typename T>
using dit_fullspace_basis = basis::basis<basis::bit_fullspace<I,J>, basis::bit_symmetry<I,T>>

template<typename I,typename J,typename K,typename T>
using dit_subspace_basis = basis::basis<basis::bit_subspace<I,J,K>, basis::bit_symmetry<I,T>>


template<typename I,typename T>
using bit_symmetry = basis::symmetry< basis::bit_perm<I>, basis::perm_bit<I>, basis::bitbasis::bit_set<I>,T>;

template<typename I,typename J,typename T>
using bit_fullspace_basis = basis::basis<basis::bit_fullspace<I,J>, basis::bit_symmetry<I,T>>

template<typename I,typename J,typename K,typename T>
using bit_subspace_basis = basis::basis<basis::bit_subspace<I,J,K>, basis::bit_symmetry<I,T>>

}

#endif