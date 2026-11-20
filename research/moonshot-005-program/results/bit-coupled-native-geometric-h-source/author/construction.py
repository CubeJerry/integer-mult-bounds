"""Complete the frozen geometric component by a 36-port general ramp."""
from pathlib import Path
import importlib.util
import json


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def require(ok, message):
    if not ok:
        raise ValueError(message)


def context(repo):
    component = module(Path(__file__).parent.parent / "component/construction.py", "full_geometric_component")
    return component, *component.context(repo)


def build(component, families, atlas, previous, prm):
    component_prm = json.loads((Path(__file__).parent.parent / "component/output/PARAMETERS.json").read_text())
    first = component.build(families, atlas, previous, component_prm)
    chart = families.Chart(atlas, prm["H"], 12)
    ports = [d for d, D in enumerate(atlas.charts)
             if atlas.planes[chart.h] <= D and d not in first["chart"].ports]
    require(ports == prm["complementary_ports"] and len(ports) == 36, "all remaining actual D exits")
    chart.ports = ports
    chart.radical = {d: sorted(set(atlas.spread["D_radicals"][d]) - {0}) for d in ports}
    require(all(sum(x in chart.radical[d] for d in ports) == 4 for x in chart.singular),
            "four genuine remaining point incidences")
    points = chart.point_table(prm["core_seed"], prm["fill_seed"])
    maps = {j: chart.maps(points, j) for j in chart.donors}
    second = {"chart": chart, "points": points, "maps": maps, "controls": chart.controls, "Hword": chart.V}
    return {3: first, 12: second}
