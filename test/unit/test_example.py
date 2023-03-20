import unittest
import numpy as np
from tinygrad.lazy import Device
from tinygrad.tensor import Tensor
from tinygrad.helpers import dtypes

def multidevice_test(fxn):
  def ret(self):
    for device in Device._buffers:
      with self.subTest(device=device):
        try:
          Device[device]
        except Exception:
          print(f"WARNING: {device} test isn't running")
          continue
        fxn(self, device)
  return ret

class TestExample(unittest.TestCase):
  @multidevice_test
  def test_convert_to_cpu(self, device):
    a = Tensor([[1,2],[3,4]], device=device)
    assert a.numpy().shape == (2,2)
    b = a.cpu()
    assert b.numpy().shape == (2,2)

  @multidevice_test
  def test_2_plus_3(self, device):
    a = Tensor([2], device=device)
    b = Tensor([3], device=device)
    result = a + b
    print(f"{a.numpy()} + {b.numpy()} = {result.numpy()}")
    assert result.numpy()[0] == 5.

  @multidevice_test
  def test_example_readme(self, device):
    x = Tensor.eye(3, device=device, requires_grad=True)
    y = Tensor([[2.0,0,-2.0]], device=device, requires_grad=True)
    z = y.matmul(x).sum()
    z.backward()

    x.grad.numpy()  # dz/dx
    y.grad.numpy()  # dz/dy

    assert x.grad.device == device
    assert y.grad.device == device

  @multidevice_test
  def test_example_matmul(self, device):
    try:
      Device[device]
    except Exception:
      print(f"WARNING: {device} test isn't running")
      return

    x = Tensor.eye(64, device=device, requires_grad=True)
    y = Tensor.eye(64, device=device, requires_grad=True)
    z = y.matmul(x).sum()
    z.backward()

    x.grad.numpy()  # dz/dx
    y.grad.numpy()  # dz/dy

    assert x.grad.device == device
    assert y.grad.device == device

if __name__ == '__main__':
  unittest.main()