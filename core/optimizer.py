import torch

class ModelOptimizer:
    @staticmethod
    def export_to_onnx(model, dummy_input, onnx_path):
        """Export a PyTorch model to ONNX for edge device optimization"""
        torch.onnx.export(
            model, 
            dummy_input, 
            onnx_path, 
            export_params=True, 
            opset_version=12, 
            do_constant_folding=True,
            input_names=['input'], 
            output_names=['output']
        )
        return onnx_path

    @staticmethod
    def apply_quantization(model):
        """Apply dynamic quantization to reduce model size for edge deployment"""
        quantized_model = torch.quantization.quantize_dynamic(
            model, {torch.nn.Linear}, dtype=torch.qint8
        )
        return quantized_model
