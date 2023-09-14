from typing import Iterable, List, Generator

from ontolearn.utils import parametrized_performance_debugger
from owlapy.model import OWLObjectMaxCardinality, OWLObjectMinCardinality, OWLObjectSomeValuesFrom, \
    OWLObjectAllValuesFrom, OWLObjectIntersectionOf, OWLObjectUnionOf, OWLObjectPropertyExpression, OWLThing, \
    OWLNothing, OWLClass, OWLClassExpression, OWLObjectComplementOf, \
    OWLObjectExactCardinality, OWLDataAllValuesFrom, OWLDataPropertyExpression, OWLDataRange, OWLDataSomeValuesFrom, \
    OWLDataHasValue, OWLIndividual, OWLLiteral, OWLObjectHasValue


class ConceptGenerator:
    """A class that can generate some sorts of OWL Class Expressions"""

    @parametrized_performance_debugger()
    def negation_from_iterables(self, class_expressions: Iterable[OWLClassExpression]):
        """Negate a sequence of Class Expressions

        Args:
            class_expressions: iterable of class expressions to negate

        Returns:
            negated form of input

                { x \\| ( x \\equv not s} """
        for item in class_expressions:
            assert isinstance(item, OWLClassExpression)
            yield self.negation(item)

    @staticmethod
    def intersect_from_iterables(a_operands: Iterable[OWLClassExpression], b_operands: Iterable[OWLClassExpression]) \
            -> Iterable[OWLObjectIntersectionOf]:
        """ Create an intersection of each class expression in a_operands with each class expression in b_operands"""
        assert isinstance(a_operands, Generator) is False and isinstance(b_operands, Generator) is False
        seen = set()
        # TODO: if input sizes say 10^4, we can employ multiprocessing
        for i in a_operands:
            for j in b_operands:
                if (i, j) in seen:
                    continue
                i_and_j = OWLObjectIntersectionOf((i, j))
                seen.add((i, j))
                seen.add((j, i))
                yield i_and_j

    @staticmethod
    def union_from_iterables(a_operands: Iterable[OWLClassExpression],
                             b_operands: Iterable[OWLClassExpression]) -> Iterable[OWLObjectUnionOf]:
        """ Create an union of each class expression in a_operands with each class expression in b_operands"""
        assert (isinstance(a_operands, Generator) is False) and (isinstance(b_operands, Generator) is False)
        # TODO: if input sizes say 10^4, we can employ multiprocessing
        seen = set()
        for i in a_operands:
            for j in b_operands:
                if (i, j) in seen:
                    continue
                i_and_j = OWLObjectUnionOf((i, j))
                seen.add((i, j))
                seen.add((j, i))
                yield i_and_j

    # noinspection PyMethodMayBeStatic
    def intersection(self, ops: Iterable[OWLClassExpression]) -> OWLObjectIntersectionOf:
        """Create intersection of class expression

        Args:
            ops: operands of the intersection

        Returns:
            intersection with all operands (intersections are merged)
        """
        # TODO CD: I would rather prefer def intersection(self, a: OWLClassExpression, b: OWLClassExpression). This is
        # TODO CD: more advantages as one does not need to create a tuple of a list before intersection two expressions.
        operands: List[OWLClassExpression] = []
        for c in ops:
            if isinstance(c, OWLObjectIntersectionOf):
                operands.extend(c.operands())
            else:
                assert isinstance(c, OWLClassExpression)
                operands.append(c)
        # operands = _avoid_overly_redundant_operands(operands)
        return OWLObjectIntersectionOf(operands)

    # noinspection PyMethodMayBeStatic
    def union(self, ops: Iterable[OWLClassExpression]) -> OWLObjectUnionOf:
        """Create union of class expressions

        Args:
            ops: operands of the union

        Returns:
            union with all operands (unions are merged)
        """
        operands: List[OWLClassExpression] = []
        for c in ops:
            if isinstance(c, OWLObjectUnionOf):
                operands.extend(c.operands())
            else:
                assert isinstance(c, OWLClassExpression)
                operands.append(c)
        # operands = _avoid_overly_redundand_operands(operands)
        return OWLObjectUnionOf(operands)

    # noinspection PyMethodMayBeStatic
    def existential_restriction(self, filler: OWLClassExpression, property: OWLObjectPropertyExpression) \
            -> OWLObjectSomeValuesFrom:
        """Create existential restriction

        Args:
            property: property
            filler: filler of the restriction

        Returns:
            existential restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectSomeValuesFrom(property=property, filler=filler)

    # noinspection PyMethodMayBeStatic
    def universal_restriction(self, filler: OWLClassExpression, property: OWLObjectPropertyExpression) \
            -> OWLObjectAllValuesFrom:
        """Create universal restriction

        Args:
            property: property
            filler: filler of the restriction

        Returns:
            universal restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectAllValuesFrom(property=property, filler=filler)

    def has_value_restriction(self, individual: OWLIndividual, property: OWLObjectPropertyExpression) \
            -> OWLObjectHasValue:
        """Create object has value restriction

        Args:
            property: property
            individual: individual of the restriction

        Returns:
            object has value restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectHasValue(property=property, individual=individual)

    def min_cardinality_restriction(self, filler: OWLClassExpression,
                                    property: OWLObjectPropertyExpression, card: int) \
            -> OWLObjectMinCardinality:
        """Create min cardinality restriction

        Args:
            filler: filler of the restriction
            property: property
            card: cardinality of the restriction

        Returns:
            min cardinality restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectMinCardinality(cardinality=card, property=property, filler=filler)

    def max_cardinality_restriction(self, filler: OWLClassExpression,
                                    property: OWLObjectPropertyExpression, card: int) \
            -> OWLObjectMaxCardinality:
        """Create max cardinality restriction

        Args:
            filler: filler of the restriction
            property: property
            card: cardinality of the restriction

        Returns:
            max cardinality restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectMaxCardinality(cardinality=card, property=property, filler=filler)

    def exact_cardinality_restriction(self, filler: OWLClassExpression,
                                      property: OWLObjectPropertyExpression, card: int) \
            -> OWLObjectExactCardinality:
        """Create exact cardinality restriction

        Args:
            filler: filler of the restriction
            property: property
            card: cardinality of the restriction

        Returns:
            exact cardinality restriction
        """
        assert isinstance(property, OWLObjectPropertyExpression)
        return OWLObjectExactCardinality(cardinality=card, property=property, filler=filler)

    def data_existential_restriction(self, filler: OWLDataRange, property: OWLDataPropertyExpression) \
            -> OWLDataSomeValuesFrom:
        """Create data existential restriction

        Args:
            filler: filler of the restriction
            property: property

        Returns:
            data existential restriction
        """
        assert isinstance(property, OWLDataPropertyExpression)
        return OWLDataSomeValuesFrom(property=property, filler=filler)

    def data_universal_restriction(self, filler: OWLDataRange, property: OWLDataPropertyExpression) \
            -> OWLDataAllValuesFrom:
        """Create data universal restriction

        Args:
            filler: filler of the restriction
            property: property

        Returns:
            data universal restriction
        """
        assert isinstance(property, OWLDataPropertyExpression)
        return OWLDataAllValuesFrom(property=property, filler=filler)

    def data_has_value_restriction(self, value: OWLLiteral, property: OWLDataPropertyExpression) \
            -> OWLDataHasValue:
        """Create data has value restriction

        Args:
            value: value of the restriction
            property: property

        Returns:
            data has value restriction
        """
        assert isinstance(property, OWLDataPropertyExpression)
        return OWLDataHasValue(property=property, value=value)

    def negation(self, concept: OWLClassExpression) -> OWLClassExpression:
        """Create negation of a concept

        Args:
            concept: class expression

        Returns:
            negation of concept
        """
        if concept.is_owl_thing():
            return self.nothing
        elif isinstance(concept, OWLObjectComplementOf):
            return concept.get_operand()
        else:
            return concept.get_object_complement_of()

    @property
    def thing(self) -> OWLClass:
        """OWL Thing"""
        return OWLThing

    @property
    def nothing(self) -> OWLClass:
        """OWL Nothing"""
        return OWLNothing