"""
Reciprocal Rank Fusion
"""

RRF_K = 60


class ReciprocalRankFusion:

    def fuse(
        self,
        dense,
        sparse,
    ):

        scores = {}

        for rank, item in enumerate(
            dense,
            start=1,
        ):

            key = item["document"]

            if key not in scores:

                scores[key] = item.copy()

                scores[key]["rrf"] = 0

            scores[key]["rrf"] += (
                1 / (RRF_K + rank)
            )

        for rank, item in enumerate(
            sparse,
            start=1,
        ):

            key = item["document"]

            if key not in scores:

                scores[key] = item.copy()

                scores[key]["rrf"] = 0

            scores[key]["rrf"] += (
                1 / (RRF_K + rank)
            )

        merged = sorted(
            scores.values(),
            key=lambda x: x["rrf"],
            reverse=True,
        )

        return merged


rrf = ReciprocalRankFusion()