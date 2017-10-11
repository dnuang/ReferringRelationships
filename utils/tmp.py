from keras import backend as K
from ReferringRelationships.config import parse_args

import tensorflow as tf


def iou(y_true, y_pred, heatmap_threshold):
    """Measures the mean IoU of our predictions with ground truth.
    Args:
        y_true: The ground truth bounding box locations.
        y_pred: Our heatmap predictions.
        heatmap_threshold: Config specified theshold above which we consider
          a prediction to contain an object.
    Returns:
        A float containing the mean IoU of our predictions.
    """
    pred = K.cast(K.greater(y_pred, heatmap_threshold), "float32")
    intersection = y_true * pred
    union = K.cast(K.greater(y_true + pred, 0), "float32")
    iou_values = K.sum(intersection, axis=1) / (K.epsilon() + K.sum(union, axis=1))
    return K.mean(iou_values)

def iou_acc(y_true, y_pred, heatmap_threshold):
    """Measures the mean accuracy of our predictions with ground truth.
    Here we consider an object localization to be correct if it contains an
    IoU > 0.5 with the ground truth box.
    Args:
        y_true: The ground truth bounding box locations.
        y_pred: Our heatmap predictions.
        heatmap_threshold: Config specified theshold above which we consider
          a prediction to contain an object.
    Returns:
        A float containing the mean accuracy of our predictions.
    """
    pred = K.cast(K.greater(y_pred, heatmap_threshold), "float32")
    intersection = y_true * pred
    union = K.cast(K.greater(y_true + pred, 0), "float32")
    iou_values = K.sum(intersection, axis=1) / (K.epsilon() + K.sum(union, axis=1))
    acc = K.cast(K.greater(iou_values, 0.5), "float32")
    return K.mean(acc)

def iou_bbox(y_true, y_pred, heatmap_threshold, input_dim=224):
    """Measures the mean IoU of our bbox predictions with ground truth.
    Args:
        y_true: The ground truth bounding box locations.
        y_pred: Our heatmap predictions.
        heatmap_threshold: Config specified theshold above which we consider
          a prediction to contain an object.
    Returns:
        A float containing the mean accuracy of our bbox predictions.
    """
    pred = K.cast(K.greater(y_pred, heatmap_threshold), "float32")
    pred = K.reshape(pred, (-1, input_dim, input_dim))
    horiz = K.sum(pred, axis=1, keepdims=True)
    horiz = K.cast(K.greater(horiz, 0), "float32")
    mask_horiz = K.repeat_elements(horiz, input_dim, axis=1)
    vert = K.sum(pred, axis=2, keepdims=True)
    vert = K.cast(K.greater(vert, 0), "float32")
    mask_vert = K.repeat_elements(vert, input_dim, axis=2)
    mask = mask_vert * mask_horiz
    mask = K.reshape(mask, (-1, input_dim * input_dim))
    intersection = y_true * mask
    union = K.cast(K.greater(y_true + mask, 0), "float32")
    iou_values = K.sum(intersection, axis=1) / (K.epsilon() + K.sum(union, axis=1))
    return K.mean(iou_values)

def iou_bbox_3(y_true, y_pred):
    return iou_bbox(y_true, y_pred, 0.3)
    
def iou_bbox_5(y_true, y_pred):
    return iou_bbox(y_true, y_pred, 0.5)

def iou_bbox_6(y_true, y_pred):
    return iou_bbox(y_true, y_pred, 0.6)

def iou_3(y_true, y_pred):
    return iou(y_true, y_pred, 0.3)

def iou_5(y_true, y_pred):
    return iou(y_true, y_pred, 0.5)

def iou_7(y_true, y_pred):
    return iou(y_true, y_pred, 0.7)

def iou_9(y_true, y_pred):
    return iou(y_true, y_pred, 0.9)

def iou_acc_3(y_true, y_pred):
    return iou_acc(y_true, y_pred, 0.3)

def iou_acc_5(y_true, y_pred):
    return iou_acc(y_true, y_pred, 0.5)


if __name__ == "__main__":
    import numpy as np;
    x = np.random.random((3, 3))
    input_dim = 3
    y = np.array([[0., 1., 1.],[1., 1., 1.],[1., 0, 1.]])
    print(x)
    print(y)
    tf.InteractiveSession()
    print(iou_bbox(y, x, 0.6, input_dim).eval())
