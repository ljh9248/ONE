#!/usr/bin/env python

# Copyright (c) 2022 Samsung Electronics Co., Ltd. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class CONSTANT:
    __slots__ = ()  # This prevents access via __dict__.
    OPTIMIZATION_OPTS = (
        # (OPTION_NAME, HELP_MESSAGE)
        ('O1', 'enable O1 optimization pass'),
        ('convert_nchw_to_nhwc',
         'Experimental: This will convert NCHW operators to NHWC under the assumption that input model is NCHW.'
         ),
        ('expand_broadcast_const', 'expand broadcastable constant node inputs'),
        ('nchw_to_nhwc_input_shape',
         'convert the input shape of the model (argument for convert_nchw_to_nhwc)'),
        ('nchw_to_nhwc_output_shape',
         'convert the output shape of the model (argument for convert_nchw_to_nhwc)'),
        ('fold_add_v2', 'fold AddV2 op with constant inputs'),
        ('fold_cast', 'fold Cast op with constant input'),
        ('fold_dequantize', 'fold Dequantize op'),
        ('fold_dwconv', 'fold Depthwise Convolution op with constant inputs'),
        ('fold_gather', 'fold Gather op'),
        ('fold_sparse_to_dense', 'fold SparseToDense op'),
        ('forward_reshape_to_unaryop', 'Forward Reshape op'),
        ('fuse_add_with_tconv', 'fuse Add op to Transposed'),
        ('fuse_add_with_fully_connected', 'fuse Add op to FullyConnected op'),
        ('fuse_batchnorm_with_conv', 'fuse BatchNorm op to Convolution op'),
        ('fuse_batchnorm_with_dwconv', 'fuse BatchNorm op to Depthwise Convolution op'),
        ('fuse_batchnorm_with_tconv', 'fuse BatchNorm op to Transposed Convolution op'),
        ('fuse_bcq', 'apply Binary Coded Quantization'),
        ('fuse_preactivation_batchnorm',
         'fuse BatchNorm operators of pre-activations to Convolution op'),
        ('fuse_mean_with_mean', 'fuse two consecutive Mean ops'),
        ('fuse_transpose_with_mean',
         'fuse Mean with a preceding Transpose under certain conditions'),
        ('make_batchnorm_gamma_positive',
         'make negative gamma of BatchNorm to a small positive value (1e-10).'
         ' Note that this pass can change the execution result of the model.'
         ' So, use it only when the impact is known to be acceptable.'),
        ('fuse_activation_function', 'fuse Activation function to a preceding operator'),
        ('fuse_instnorm', 'fuse ops to InstanceNorm operator'),
        ('replace_cw_mul_add_with_depthwise_conv',
         'replace channel-wise Mul/Add with DepthwiseConv2D'),
        ('remove_fakequant', 'remove FakeQuant ops'),
        ('remove_quantdequant', 'remove Quantize-Dequantize sequence'),
        ('remove_redundant_quantize', 'remove redundant Quantize ops'),
        ('remove_redundant_reshape', 'fuse or remove subsequent Reshape ops'),
        ('remove_redundant_transpose', 'fuse or remove subsequent Transpose ops'),
        ('remove_unnecessary_reshape', 'remove unnecessary reshape ops'),
        ('remove_unnecessary_slice', 'remove unnecessary slice ops'),
        ('remove_unnecessary_strided_slice', 'remove unnecessary strided slice ops'),
        ('remove_unnecessary_split', 'remove unnecessary split ops'),
        ('replace_non_const_fc_with_batch_matmul', 'replace FullyConnected op with non-const weights to BatchMatMul op'),
        ('resolve_customop_add', 'convert Custom(Add) op to Add op'),
        ('resolve_customop_batchmatmul',
         'convert Custom(BatchMatmul) op to BatchMatmul op'),
        ('resolve_customop_matmul', 'convert Custom(Matmul) op to Matmul op'),
        ('resolve_customop_max_pool_with_argmax',
         'convert Custom(MaxPoolWithArgmax) to net of builtin operators'),
        ('shuffle_weight_to_16x1float32',
         'convert weight format of FullyConnected op to SHUFFLED16x1FLOAT32.'
         ' Note that it only converts weights whose row is a multiple of 16'),
        ('substitute_pack_to_reshape', 'convert single input Pack op to Reshape op'),
        ('substitute_padv2_to_pad', 'convert certain condition PadV2 to Pad'),
        ('substitute_splitv_to_split', 'convert certain condition SplitV to Split'),
        ('substitute_squeeze_to_reshape', 'convert certain condition Squeeze to Reshape'),
        ('substitute_strided_slice_to_reshape',
         'convert certain condition StridedSlice to Reshape'),
        ('substitute_transpose_to_reshape',
         'convert certain condition Transpose to Reshape'),
        ('transform_min_max_to_relu6', 'transform Minimum-Maximum pattern to Relu6 op'),
        ('transform_min_relu_to_relu6', 'transform Minimum(6)-Relu pattern to Relu6 op'))


CONSTANT = CONSTANT()
