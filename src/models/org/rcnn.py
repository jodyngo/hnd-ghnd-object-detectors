from torchvision.models.detection.backbone_utils import resnet_fpn_backbone
from torchvision.models.detection.faster_rcnn import FasterRCNN
from torchvision.models.detection.keypoint_rcnn import KeypointRCNN
from torchvision.models.detection.mask_rcnn import MaskRCNN
from torchvision.models.utils import load_state_dict_from_url

MODEL_URL_DICT = {
    'fasterrcnn_resnet50_fpn_coco':
        'https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth',
    'maskrcnn_resnet50_fpn_coco':
        'https://download.pytorch.org/models/maskrcnn_resnet50_fpn_coco-bf2d0c1e.pth',
    'keypointrcnn_resnet50_fpn_coco':
        'https://download.pytorch.org/models/keypointrcnn_resnet50_fpn_coco-9f466800.pth'
}

MODEL_CLASS_DICT = {
    'faster_rcnn': (FasterRCNN, 'fasterrcnn_resnet50_fpn_coco'),
    'mask_rcnn': (MaskRCNN, 'maskrcnn_resnet50_fpn_coco'),
    'keypoint_rcnn': (KeypointRCNN, 'keypointrcnn_resnet50_fpn_coco')
}


def get_model_config(model_name):
    if model_name in MODEL_CLASS_DICT:
        return MODEL_CLASS_DICT[model_name]
    raise KeyError('model_name `{}` is not expected'.format(model_name))


def get_model(model_name, pretrained, backbone_name=None, backbone_pretrained=True,
                   progress=True, num_classes=91, **kwargs):
    if pretrained:
        backbone_pretrained = False

    backbone = resnet_fpn_backbone(backbone_name, backbone_pretrained)
    model_class, pretrained_key = get_model_config(model_name)
    model = model_class(backbone, num_classes, **kwargs)
    if pretrained and backbone_name == 'resnet50':
        state_dict = load_state_dict_from_url(MODEL_URL_DICT[pretrained_key], progress=progress)
        model.load_state_dict(state_dict)
    return model