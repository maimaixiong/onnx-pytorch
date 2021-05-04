import onnx
import torch
from onnx.numpy_helper import to_array

from onnx_pytorch.op_code_generators import OpCodeGenerator


class ConcatOpCodeGenerator(OpCodeGenerator):

  def __init__(self,
               onnx_ver=onnx.defs.onnx_opset_version(),
               torch_ver=torch.__version__):
    super(ConcatOpCodeGenerator, self).__init__(onnx_ver, torch_ver)

  def gen(self, node, value_infos, initializers):
    attr_value_dict = self.get_attr_value_dict(node)
    inputs_str, outputs_str = self.gen_input_output_string(node, initializers)
    init_str, forward_str = [], []
    axis = attr_value_dict["axis"]
    params_str = self.gen_params_str(dim=axis)
    forward_str.append(
        f"{', '.join(outputs_str)} = torch.cat(({', '.join(inputs_str)}), **{{{params_str}}})")
    return {"init": init_str, "forward": forward_str}