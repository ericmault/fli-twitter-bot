## TO-DO

@pytest.fixture
def input_value():
   input = 39
   return input

@pytest.mark.parametrize("num, output",[(1,11),(2,22),(3,35),(4,44)])
def test_multiplication_11(num, output):
   assert 11*num == output




def test_mytest():
    a = 1
    b = 2
    assert a+b==3
