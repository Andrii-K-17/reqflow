import uuid

from app.models.enums import DEPENDENCY_RELATIONS, TraceEntityType
from app.models.trace_link import TraceLink
from app.repositories.trace_link_repository import TraceLinkRepository
from app.schemas.trace_link import TraceGraph, TraceGraphEdge, TraceGraphNode, TraceLinkCreate
from app.services.entity_resolver import EntityResolver


class EntityNotFoundError(Exception):
    pass


class DuplicateTraceLinkError(Exception):
    pass


class TraceCycleError(Exception):
    pass


class TraceabilityService:
    def __init__(self, trace_links: TraceLinkRepository, resolver: EntityResolver) -> None:
        self._trace_links = trace_links
        self._resolver = resolver

    async def create_link(self, *, project_id: uuid.UUID, payload: TraceLinkCreate) -> TraceLink:
        if not await self._resolver.exists(
            project_id=project_id,
            entity_type=payload.from_type,
            entity_id=payload.from_id,
        ):
            raise EntityNotFoundError(f"{payload.from_type} {payload.from_id} not found in project")

        if not await self._resolver.exists(
            project_id=project_id,
            entity_type=payload.to_type,
            entity_id=payload.to_id,
        ):
            raise EntityNotFoundError(f"{payload.to_type} {payload.to_id} not found in project")

        if await self._trace_links.exists(
            project_id=project_id,
            from_type=payload.from_type,
            from_id=payload.from_id,
            to_type=payload.to_type,
            to_id=payload.to_id,
            relation=payload.relation,
        ):
            raise DuplicateTraceLinkError("This trace link already exists")

        if payload.relation in DEPENDENCY_RELATIONS:
            existing_links = await self._trace_links.list_for_project(project_id)
            if self._would_create_cycle(existing_links, payload):
                raise TraceCycleError(
                    "This link would create a circular dependency in the traceability graph"
                )

        link = TraceLink(
            project_id=project_id,
            from_type=payload.from_type,
            from_id=payload.from_id,
            to_type=payload.to_type,
            to_id=payload.to_id,
            relation=payload.relation,
        )
        self._trace_links.add(link)
        await self._trace_links.flush()
        return link

    @staticmethod
    def _would_create_cycle(existing_links: list[TraceLink], new_link: TraceLinkCreate) -> bool:
        """Check if adding new_link (from -> to) introduces a circular dependency.

        Uses iterative DFS to determine if a path from `to` back to `from`
        already exists through dependency relations.
        """
        adjacency: dict[
            tuple[TraceEntityType, uuid.UUID], list[tuple[TraceEntityType, uuid.UUID]]
        ] = {}
        for link in existing_links:
            if link.relation not in DEPENDENCY_RELATIONS:
                continue
            adjacency.setdefault((link.from_type, link.from_id), []).append(
                (link.to_type, link.to_id)
            )

        target = (new_link.from_type, new_link.from_id)
        start = (new_link.to_type, new_link.to_id)

        visited: set[tuple[TraceEntityType, uuid.UUID]] = set()
        stack = [start]
        while stack:
            current = stack.pop()
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            stack.extend(adjacency.get(current, []))

        return False

    async def list_links(self, project_id: uuid.UUID) -> list[TraceLink]:
        return await self._trace_links.list_for_project(project_id)

    async def delete_link(self, *, project_id: uuid.UUID, link_id: uuid.UUID) -> bool:
        link = await self._trace_links.get(project_id=project_id, link_id=link_id)
        if link is None:
            return False
        await self._trace_links.delete(link)
        await self._trace_links.flush()
        return True

    async def build_graph(self, project_id: uuid.UUID) -> TraceGraph:
        """Construct a full visual graph of project trace links and their resolved entities."""
        links = await self._trace_links.list_for_project(project_id)

        node_keys: set[tuple[TraceEntityType, uuid.UUID]] = set()
        for link in links:
            node_keys.add((link.from_type, link.from_id))
            node_keys.add((link.to_type, link.to_id))

        nodes: list[TraceGraphNode] = []
        for entity_type, entity_id in node_keys:
            label = await self._resolver.resolve_label(
                project_id=project_id, entity_type=entity_type, entity_id=entity_id
            )
            if label is None:
                continue
            nodes.append(
                TraceGraphNode(
                    id=entity_id,
                    type=entity_type,
                    code=label.code,
                    label=label.label,
                )
            )

        edges = [
            TraceGraphEdge(from_id=link.from_id, to_id=link.to_id, relation=link.relation)
            for link in links
        ]

        return TraceGraph(nodes=nodes, edges=edges)
