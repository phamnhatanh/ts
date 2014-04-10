import numpy
from math import e
from math import sqrt
from math import pi


class GaussianNB:
    def fit(self, samples, results):
        """Arguments:
            samples - list of lists, each sublist has the same length and
            contains values of features.

            results - list of classes, one for each sample in samples,
            in the same order. Each value here must first be added with
            add_classes method.
        """
        self.__check_classes(results)
        assert len(samples) == len(results)
        self.__class_prior_probabilities = {
            _class: 0.0 for _class in self.__classes}
        for result in results:
            self.__class_prior_probabilities[result] += 1.0 / len(results)

        # calculate mean and variance of each feature for each class
        total_features = len(samples[0])
        self.__means = {}
        self.__variances = {}
        for _class in self.__classes:
            samples_of_this_class = [
                sample for sample, result in zip(samples, results)
                if result == _class]

            for feature_index in range(total_features):
                feature_values = [
                    sample[feature_index] for sample in samples_of_this_class]
                self.__means[(_class, feature_index)] = numpy.mean(
                    feature_values)
                self.__variances[(_class, feature_index)] = gaussian_variance(
                    feature_values)

    def __check_classes(self, results):
        for result in results:
            if result not in self.classes:
                raise Exception("{} - no such class".format(result))

    def predict(self, sample):
        predicted_probabilities = {
            self.__classes_prior_probabilities[_class] *
            numpy.prod([
                GaussianNB.__gaussian_likelihood(
                    value,
                    self.__means[(_class, index)],
                    self.__variances[(_class, index)]
                )
                for value, index in zip(sample, range(len(sample)))
            ]):
            _class
            for _class in self.__classes
        }
        return predicted_probabilities[max(predicted_probabilities.keys())]

    @staticmethod
    def __gaussian_likelihood(value, mean, variance):
        if value is None:
            return 1
        return (e ** (-1) * ((float(value) - mean) ** 2) / (2 * variance)) / \
            sqrt(2.0 * pi * variance)

    def add_classes(self, classes):
        """Manually configure, how big the classes for our regression are,
        for example 0-10, 11-20, 21-30, etc.

        Arguments:
            classes - list of pairs, each pair corresponds to min and max
            values of that class (for example (0,10) corresponds to 0-10.
            Must not overlap, each next pair's values must be bigger than
            previous pair's values
        """
        self.__classes = classes


def gaussian_variance(numbers):
    mean = numpy.mean(numbers)
    squared_differences = (numbers - mean) ** 2
    return sum(squared_differences) / len(numbers)
