"""
This is a boilerplate pipeline 'model_evaluation'
generated using Kedro 0.18.8
"""
import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, precision_recall_curve, auc, f1_score
import mlflow
from mlflow import sklearn


def evaluate_model(y_test, y_pred):

    def get_auc(labels, scores):
        fpr, tpr, thr = roc_curve(labels, scores)
        auc_score = auc(fpr, tpr)
        return fpr, tpr, auc_score

    def get_aucpr(labels, scores):
        precision, recall, th = precision_recall_curve(labels, scores)
        aucpr_score = np.trapz(recall, precision)
        return precision, recall, aucpr_score

    def plot_metric(ax, x, y, x_label, y_label, plot_label, style="-"):
        ax.plot(x, y, style, label=plot_label)
        ax.legend()
        ax.set_ylabel(x_label)
        ax.set_xlabel(y_label)

    def prediction_summary(labels, predicted_score, info, plot_baseline=True, axes=None):
        if axes is None:
            axes = [plt.subplot(1, 2, 1), plt.subplot(1, 2, 2)]
        fpr, tpr, auc_score = get_auc(labels, predicted_score)
        plot_metric(axes[0], fpr, tpr, "False positive rate", "True positive rate", "{} AUC={:.4f}".format(info, auc_score))
        if plot_baseline:
            plot_metric(axes[0], [0, 1], [0, 1], "False positive rate", "True positive rate", "Baseline AUC=0.5", "r--")
        precision, recall, aucpr_score = get_aucpr(labels, predicted_score)
        plot_metric(axes[1], recall, precision, "Recall", "Precision", "{} AUCPR={:.4f}".format(info, aucpr_score))
        if plot_baseline:
            thr = np.sum(labels) / len(labels)
            thr = float(thr)
            plot_metric(axes[1], [0, 1], [thr, thr], "Recall", "Precision", "Baseline AUCPR={:.4f}".format(thr), "r--")

        # Add F1 score as text on top of the plot
        f1 = f1_score(labels, predicted_score)
        f1_text = "F1-score: {:.4f}".format(f1)
        axes[1].text(0.5, 1.05, f1_text, ha='center', va='center', transform=axes[1].transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2'))

        plt.show()
        return axes


    fpr, tpr, auc_score = get_auc(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    log = logging.getLogger(__name__)
    log.info("Model auc score on test set: %0.2f%%", auc_score)
    log.info("Model f1-score on test set: %0.2f%%", f1)

    metrics = {"f1_score": f1, "auc_score": auc_score}

    fig = plt.figure()
    fig.set_figheight(4.5)
    fig.set_figwidth(4.5 * 2)
    axes = prediction_summary(y_test, y_pred, "Random Forest")
    #mlflow.end_run()

    return fig, metrics

