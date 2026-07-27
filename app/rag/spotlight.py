"""
Context Spotlight Builder
"""

import logging

logger = logging.getLogger(__name__)


class Spotlight:

    def build_context(
        self,
        documents,
        web_results=None,
    ):

        context = []

        for index, doc in enumerate(
            documents,
            start=1,
        ):

            context.append(
                f"""
<Document {index}>

{doc["document"]}

</Document {index}>
"""
            )

        if web_results:

            for index, item in enumerate(
                web_results,
                start=len(context) + 1,
            ):

                context.append(
                    f"""
<Web {index}>

Title:
{item.get("title","")}

Content:
{item.get("content","")}

URL:
{item.get("url","")}

</Web {index}>
"""
                )

        return "\n".join(
            context
        )


spotlight = Spotlight()