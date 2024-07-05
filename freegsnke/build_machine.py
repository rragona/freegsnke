import os
import pickle

import numpy as np
from freegsfast.coil import Coil
from freegsfast.machine import Circuit, Solenoid, Wall
from freegsfast.multi_coil import MultiCoil

from .machine_update import Machine
from .magnetic_probes import Probes
from .passive_structure import PassiveStructure
from .refine_passive import generate_refinement

default_min_refine_per_area = 3e3
default_min_refine_per_length = 200

passive_coils_path = os.environ.get("PASSIVE_COILS_PATH", None)
if passive_coils_path is None:
    raise ValueError("PASSIVE_COILS_PATH environment variable not set.")

active_coils_path = os.environ.get("ACTIVE_COILS_PATH", None)
if active_coils_path is None:
    raise ValueError("ACTIVE_COILS_PATH environment variable not set.")

wall_path = os.environ.get("WALL_PATH", None)
if wall_path is None:
    raise ValueError("WALL_PATH environment variable not set.")

limiter_path = os.environ.get("LIMITER_PATH", None)
if limiter_path is None:
    raise ValueError("LIMITER_PATH environment variable not set.")

with open(passive_coils_path, "rb") as f:
    passive_coils = pickle.load(f)

with open(active_coils_path, "rb") as f:
    active_coils = pickle.load(f)

with open(wall_path, "rb") as f:
    wall = pickle.load(f)

with open(limiter_path, "rb") as f:
    limiter = pickle.load(f)

if "Solenoid" not in active_coils:
    # raise ValueError("No Solenoid in active coils. Must be capitalised Solenoid.")
    print("No coil named Solenoid among the active coils.")


def tokamak(refine_mode="G", group_filaments=True):
    """MAST-Upgrade, using MultiCoil to represent coils with different locations
    for each strand.

    Parameters
    ----------
    refine_mode : str, optional
        refinement mode for passive structures inputted as polygons, by default 'G' for 'grid'
        Use 'LH' for alternative mode using a Latin Hypercube implementation.
    group_filaments : bool, optional
        If True, filaments generated by each refined passive structure are kept grouped,
        implying that they will share the same uniform current distribution. By default True.

    Returns
    -------
    FreeGSNKE tokamak machine object.
    """
    coils = []
    for coil_name in active_coils:
        if coil_name == "Solenoid":
            # Add the solenoid if any
            multicoil = MultiCoil(
                active_coils["Solenoid"]["R"], active_coils["Solenoid"]["Z"]
            )
            multicoil.dR = active_coils["Solenoid"]["dR"]
            multicoil.dZ = active_coils["Solenoid"]["dZ"]
            coils.append(
                (
                    "Solenoid",
                    Circuit(
                        [
                            (
                                "Solenoid",
                                multicoil,
                                float(active_coils["Solenoid"]["polarity"])
                                * float(active_coils["Solenoid"]["multiplier"]),
                            ),
                        ]
                    ),
                ),
            )

        else:
            # Add active coils
            circuit_list = []
            for ind in active_coils[coil_name]:
                multicoil = MultiCoil(
                    active_coils[coil_name][ind]["R"],
                    active_coils[coil_name][ind]["Z"],
                )
                multicoil.dR = active_coils[coil_name][ind]["dR"]
                multicoil.dZ = active_coils[coil_name][ind]["dZ"]
                circuit_list.append(
                    (
                        coil_name + ind,
                        multicoil,
                        float(active_coils[coil_name][ind]["polarity"])
                        * float(active_coils[coil_name][ind]["multiplier"]),
                    )
                )
            coils.append(
                (
                    coil_name,
                    Circuit(circuit_list),
                )
            )

    coils_dict = build_active_coil_dict(active_coils=active_coils)
    coils_list = list(coils_dict.keys())

    # Add passive coils
    for i, coil in enumerate(passive_coils):
        # include name if provided
        try:
            coil_name = coil["name"]
        except:
            coil_name = f"passive_{i}"
        coils_list.append(coil_name)
        # print(coil_name)

        if np.size(coil["R"]) > 1:
            # refine if vertices provided

            if group_filaments:
                # keep refinement filaments grouped
                # i.e. use new passive structure class
                try:
                    min_refine_per_area = 1.0 * coil["min_refine_per_area"]
                except:
                    min_refine_per_area = 1.0 * default_min_refine_per_area
                try:
                    min_refine_per_length = 1.0 * coil["min_refine_per_length"]
                except:
                    min_refine_per_length = 1.0 * default_min_refine_per_length

                ps = PassiveStructure(
                    R=coil["R"],
                    Z=coil["Z"],
                    min_refine_per_area=min_refine_per_area,
                    min_refine_per_length=min_refine_per_length,
                )
                coils.append(((coil_name, ps)))

                # add coil_dict entry
                coils_dict[coil_name] = {}
                coils_dict[coil_name]["active"] = False
                coils_dict[coil_name]["vertices"] = np.array((coil["R"], coil["Z"]))
                coils_dict[coil_name]["coords"] = np.array(
                    [ps.filaments[:, 0], ps.filaments[:, 1]]
                )
                coils_dict[coil_name]["area"] = ps.area
                filament_size = (ps.area / len(ps.filaments)) ** 0.5
                coils_dict[coil_name]["dR"] = filament_size
                coils_dict[coil_name]["dZ"] = filament_size
                coils_dict[coil_name]["polarity"] = np.array([1])
                # here 'multiplier' is used to normalise the green functions,
                # this is needed because currents are distributed over the passive structure
                coils_dict[coil_name]["multiplier"] = np.array([1 / len(ps.filaments)])
                # this is resistivity divided by area
                coils_dict[coil_name]["resistivity"] = (
                    coil["resistivity"] / coils_dict[coil_name]["area"]
                )

            else:
                # splits structure to individual filaments
                # each with their own current values
                filaments, area = generate_refinement(
                    R=coil["R"], Z=coil["Z"], n_refine=None, mode=refine_mode
                )
                n_filaments = len(filaments)
                filament_size = (area / n_filaments) ** 0.5

                for k, filament in enumerate(filaments):
                    filament_name = coil_name + str(k)
                    coils.append(
                        (
                            (
                                filament_name,
                                Coil(
                                    R=filament[0],
                                    Z=filament[1],
                                    area=area / n_filaments,
                                    control=False,
                                ),
                            )
                        )
                    )
                    # add coil_dict entry
                    coils_dict[filament_name] = {}
                    coils_dict[filament_name]["active"] = False
                    coils_dict[filament_name]["coords"] = np.array(
                        (filament[0], filament[1])
                    )[:, np.newaxis]
                    coils_dict[filament_name]["dR"] = filament_size
                    coils_dict[filament_name]["dZ"] = filament_size
                    coils_dict[filament_name]["polarity"] = np.array([1])
                    coils_dict[filament_name]["multiplier"] = np.array([1])
                    # this is resistivity divided by area
                    coils_dict[filament_name]["resistivity"] = coil["resistivity"] / (
                        area / n_filaments
                    )

        else:
            # passive structure is not refined
            coils.append(
                (
                    (
                        coil_name,
                        Coil(
                            R=coil["R"],
                            Z=coil["Z"],
                            area=coil["dR"] * coil["dZ"],
                            control=False,
                        ),
                    )
                )
            )
            # add coil_dict entry
            coils_dict[coil_name] = {}
            coils_dict[coil_name]["active"] = False
            coils_dict[coil_name]["coords"] = np.array((coil["R"], coil["Z"]))[
                :, np.newaxis
            ]
            coils_dict[coil_name]["dR"] = coil["dR"]
            coils_dict[coil_name]["dZ"] = coil["dZ"]
            coils_dict[coil_name]["polarity"] = np.array([1])
            coils_dict[coil_name]["multiplier"] = np.array([1])
            # this is resistivity divided by area
            coils_dict[coil_name]["resistivity"] = coil["resistivity"] / (
                coil["dR"] * coil["dZ"]
            )

    # # Add passive coils (old: filaments only)
    # for i, coil in enumerate(passive_coils):
    #     try:
    #         coil_name = coil["name"]
    #     except:
    #         coil_name = f"passive_{i}"
    #     coils.append(
    #         (
    #             (
    #                 coil_name,
    #                 Coil(
    #                     R=coil["R"],
    #                     Z=coil["Z"],
    #                     area=coil["dR"] * coil["dZ"],
    #                     control=False,
    #                 ),
    #             )
    #         )
    #     )

    # Add walls
    r_wall = [entry["R"] for entry in wall]
    z_wall = [entry["Z"] for entry in wall]

    # Add limiter
    r_limiter = [entry["R"] for entry in limiter]
    z_limiter = [entry["Z"] for entry in limiter]

    tokamak_machine = Machine(
        coils, wall=Wall(r_wall, z_wall), limiter=Wall(r_limiter, z_limiter)
    )

    tokamak_machine.coils_dict = coils_dict
    tokamak_machine.coils_list = coils_list

    # Number of active coils
    tokamak_machine.n_active_coils = len(active_coils)
    # Total number of coils
    tokamak_machine.n_coils = len(list(coils_dict.keys()))

    # Save coils_dict
    machine_path = os.path.join(
        os.path.split(active_coils_path)[0], "machine_data.pickle"
    )
    with open(machine_path, "wb") as f:
        pickle.dump(coils_dict, f)

    # add probe object attribute to tokamak
    tokamak_machine.probes = Probes(coils_dict)

    return tokamak_machine


def build_active_coil_dict(active_coils):
    """Adds vectorised properties of all active coils to a dictionary for use throughout FreeGSNKE.

    Parameters
    ----------
    active_coils : dictionary
        input dictionary, user defined with properties of the active coils

    Returns
    -------
    dictionary
        includes vectorised properties of all active coils
    """

    coils_dict = {}
    for i, coil_name in enumerate(active_coils):
        if coil_name == "Solenoid":
            coils_dict[coil_name] = {}
            coils_dict[coil_name]["active"] = True
            coils_dict[coil_name]["coords"] = np.array(
                [active_coils[coil_name]["R"], active_coils[coil_name]["Z"]]
            )
            coils_dict[coil_name]["polarity"] = np.array(
                [active_coils[coil_name]["polarity"]]
                * len(active_coils[coil_name]["R"])
            )
            coils_dict[coil_name]["dR"] = active_coils[coil_name]["dR"]
            coils_dict[coil_name]["dZ"] = active_coils[coil_name]["dZ"]
            # this is resistivity divided by area
            coils_dict[coil_name]["resistivity"] = active_coils[coil_name][
                "resistivity"
            ] / (active_coils[coil_name]["dR"] * active_coils[coil_name]["dZ"])
            coils_dict[coil_name]["multiplier"] = np.array(
                [active_coils[coil_name]["multiplier"]]
                * len(active_coils[coil_name]["R"])
            )
            continue

        coils_dict[coil_name] = {}
        coils_dict[coil_name]["active"] = True

        coords_R = []
        for ind in active_coils[coil_name].keys():
            coords_R.extend(active_coils[coil_name][ind]["R"])

        coords_Z = []
        for ind in active_coils[coil_name].keys():
            coords_Z.extend(active_coils[coil_name][ind]["Z"])
        coils_dict[coil_name]["coords"] = np.array([coords_R, coords_Z])

        polarity = []
        for ind in active_coils[coil_name].keys():
            polarity.extend(
                [active_coils[coil_name][ind]["polarity"]]
                * len(active_coils[coil_name][ind]["R"])
            )
        coils_dict[coil_name]["polarity"] = np.array(polarity)

        multiplier = []
        for ind in active_coils[coil_name].keys():
            multiplier.extend(
                [active_coils[coil_name][ind]["multiplier"]]
                * len(active_coils[coil_name][ind]["R"])
            )
        coils_dict[coil_name]["multiplier"] = np.array(multiplier)

        coils_dict[coil_name]["dR"] = active_coils[coil_name][
            list(active_coils[coil_name].keys())[0]
        ]["dR"]
        coils_dict[coil_name]["dZ"] = active_coils[coil_name][
            list(active_coils[coil_name].keys())[0]
        ]["dZ"]

        # this is resistivity divided by area
        coils_dict[coil_name]["resistivity"] = active_coils[coil_name][
            list(active_coils[coil_name].keys())[0]
        ]["resistivity"] / (coils_dict[coil_name]["dR"] * coils_dict[coil_name]["dZ"])

    return coils_dict


if __name__ == "__main__":
    # tokamak = tokamak()
    for coil_name in active_coils:
        print([pol for pol in active_coils[coil_name]])
