from quspin_core.symmetry import symmetry_api
from quspin_core._symmetry_utils import (
    check_bit_lat_args,
    check_dit_lat_args,
    check_bit_loc_args,
    check_dit_loc_args,
    check_bit_args,
    check_dit_args,
    check_args
)
import unittest
import numpy as np



class TestSymmetryAPI(unittest.TestCase):
    def assertArrayEqual(self,first,second,msg=None):
        self.assertTrue(np.all(first==second),msg=msg)
    
    def get_bit_lat_args(self):
        chars = [1,-1,1]
        args = [
            [0,1,2],
            [1,2,0],
            [2,0,1],
            ]
        return args,chars,args,np.asarray(chars,dtype=np.complex128)
    
    def get_bit_loc_args(self):
        chars = [1,-1,1]
        args = [
            [False,True ,False],
            [True ,True ,False],
            [True ,False,True ],
            ]
        return args,chars,args,np.asarray(chars,dtype=np.complex128)
    
    def get_dit_lat_args(self):
        lhss = 3
        chars = [1,-1,1]
        args = [
            [0,1,2],
            [1,2,0],
            [2,0,1],
            ]
        return lhss,args,chars,args,np.asarray(chars,dtype=np.complex128)
    
    def get_dit_loc_args(self):
        lhss = 3
        args = [
            ([[0,1,2]],[1]),
            ([[0,1,2],[1,2,0]],[0,2]),
            ([[0,1,2],[1,2,0],[2,0,1]],[0,2,5]),
        ]
        chars = [1,2,3]
        
        return lhss,args,chars,args,np.asarray(chars,dtype=np.complex128)
    
    def test_check_bit_lat_args(self):
        # proper arguments
        args,chars,test_args,test_chars = self.get_bit_lat_args()

        result_args,result_chars = check_bit_lat_args(args,chars)
        self.assertEqual(result_args,test_args)
        self.assertArrayEqual(test_chars,result_chars)
        self.assertRaises(ValueError,check_bit_lat_args,args,[1,2,3,4])
    
    def test_check_dit_lat_args(self):
        # proper arguments
        lhss = 3
        chars = [1,-1,1]
        args = [
            [0,1,2],
            [1,2,0],
            [2,0,1],
            ]
        
        test_chars = np.array([1,-1,1],dtype=np.complex128)
        test_args = args
        
        result_args,result_chars = check_dit_lat_args(lhss,args,chars)
        self.assertEqual(result_args,test_args)
        self.assertArrayEqual(test_chars,result_chars)
        self.assertRaises(ValueError,check_dit_lat_args,lhss,args,[1,2,3,4])
    
    def test_check_bit_loc_args(self):
        # proper arguments
        args,chars,test_args,test_chars = self.get_bit_loc_args()
        
        int_args = [
            [0,1,0],
            [1,1,0],
            [1,0,1],
            ]

        
        result_args,result_chars = check_bit_loc_args(args,chars)
        self.assertEqual(result_args,test_args)
        self.assertArrayEqual(test_chars,result_chars)
        self.assertRaises(ValueError,check_bit_loc_args,args,[1,2,3,4])
        self.assertRaises(TypeError,check_bit_loc_args,int_args,chars)
    
    def test_check_dit_loc_args(self):
        lhss,args,chars,test_args,test_chars = self.get_dit_loc_args()
        result_args,result_chars = check_dit_loc_args(lhss,args,chars)
        
        self.assertEqual(result_args,test_args)
        self.assertArrayEqual(result_chars,test_chars)
        self.assertRaises(ValueError,check_dit_loc_args,lhss+1,args,chars)
        self.assertRaises(ValueError,check_dit_loc_args,lhss,args,[1,2,3,4])
        bad_args  = [
            ([0,1,2],[1]),
            ([[0,1,2],[1,2,0]],[0,2]),
            ([[0,1,2],[1,2,0],[2,0,1]],[0,2,5]),
        ]
        self.assertRaises(ValueError,check_dit_loc_args,lhss,bad_args,chars)

        bad_args  = [
            ([0,1,2],[1]),
            ([[0,1,2],[1,2,0]],[0,2]),
            ([[0,1,2],[1,2,0],[2,0,1]],[0,2,5]),
        ]
        self.assertRaises(ValueError,check_dit_loc_args,lhss,bad_args,chars)
        
        bad_args  = [
            ([[0,1,2]],[[1]]),
            ([[0,1,2],[1,2,0]],[0,2]),
            ([[0,1,2],[1,2,0],[2,0,1]],[0,2,5]),
        ]
        self.assertRaises(ValueError,check_dit_loc_args,lhss,bad_args,chars)
        
        bad_args  = [
            ([[0,1,2]],[1,0]),
            ([[0,1,2],[1,2,0]],[0,2]),
            ([[0,1,2],[1,2,0],[2,0,1]],[0,2,5]),
        ]
        self.assertRaises(ValueError,check_dit_loc_args,lhss,bad_args,chars)    
    
    def test_check_bit_args(self):
        lat_args,lat_chars,test_lat_args,test_lat_chars = self.get_bit_lat_args()
        loc_args,loc_chars,test_loc_args,test_loc_chars = self.get_bit_loc_args()

        
        (result_lat_args,
         result_lat_chars,
         result_loc_args,
         result_loc_chars) = check_bit_args(lat_args,lat_chars,loc_args,loc_chars)
        
        self.assertEqual(test_lat_args,result_lat_args)
        self.assertEqual(test_loc_args,result_loc_args)
        self.assertArrayEqual(test_lat_chars,result_lat_chars)
        self.assertArrayEqual(test_loc_chars,result_loc_chars)
 
    def test_check_dit_args(self):
        _   ,lat_args,lat_chars,test_lat_args,test_lat_chars = self.get_dit_lat_args()
        lhss,loc_args,loc_chars,test_loc_args,test_loc_chars = self.get_dit_loc_args()
        
        (result_lat_args,
         result_lat_chars,
         result_loc_args,
         result_loc_chars) = check_dit_args(lhss,lat_args,lat_chars,loc_args,loc_chars)
        
        self.assertEqual(test_lat_args,result_lat_args)
        self.assertEqual(test_loc_args,result_loc_args)
        self.assertArrayEqual(test_lat_chars,result_lat_chars)
        self.assertArrayEqual(test_loc_chars,result_loc_chars)
    
    def test_check_args(self):
        _   ,lat_args,lat_chars,test_lat_args,test_lat_chars = self.get_dit_lat_args()
        lhss,loc_args,loc_chars,test_loc_args,test_loc_chars = self.get_dit_loc_args()
        
        (result_lat_args,
         result_lat_chars,
         result_loc_args,
         result_loc_chars) = check_dit_args(lhss,lat_args,lat_chars,loc_args,loc_chars)
        
        self.assertEqual(test_lat_args,result_lat_args)
        self.assertEqual(test_loc_args,result_loc_args)
        self.assertArrayEqual(test_lat_chars,result_lat_chars)
        self.assertArrayEqual(test_loc_chars,result_loc_chars)
        
        # bits

        lat_args,lat_chars,test_lat_args,test_lat_chars = self.get_bit_lat_args()
        loc_args,loc_chars,test_loc_args,test_loc_chars = self.get_bit_loc_args()

        (result_lat_args,
         result_lat_chars,
         result_loc_args,
         result_loc_chars) = check_bit_args(lat_args,lat_chars,loc_args,loc_chars)
        
        self.assertEqual(test_lat_args,result_lat_args)
        self.assertEqual(test_loc_args,result_loc_args)
        self.assertArrayEqual(test_lat_chars,result_lat_chars)
        self.assertArrayEqual(test_loc_chars,result_loc_chars)
        
        self.assertRaises(ValueError,check_args,1,lat_args,lat_chars,loc_args,loc_chars)
        
        
    def test_symmetry_constructor(self):
        lat_args,lat_chars,*_ = self.get_bit_lat_args()
        loc_args,loc_chars,*_ = self.get_bit_loc_args()
        args = 2,16,lat_args,lat_chars,loc_args,loc_chars
        self.assertRaises(
            ValueError,
            symmetry_api,
            *args
        )