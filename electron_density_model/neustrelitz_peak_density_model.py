import math


class LocalTimeF1:
    """
    Represents a class for calculating variations in local time, solar zenith angles, and local time variation factor F1.

    This class provides methods to calculate diurnal, semi-diurnal, and ter-diurnal harmonic components related to variations in local time,
    various angles related to solar zenith angles based on geographic latitude and sun declination,
    the local time at the beginning of the bite out, summer daytime bite-out effect,
    and integrates these results to compute the local time variation factor F1.

    Attributes
    ----------
    local_time_hours : int
        The local time in hours for which variations are calculated.
    latitude_radians : float
        The geographic latitude in radians.
    sun_declination_radians : float
        The sun's declination angle in radians.
    day_of_year : int
        The day of the year for which calculations are performed.
    coefficients : list
        Coefficients used in the F1 calculation.

    Methods
    -------
    calculate_local_time_variations() -> Tuple[float, float, float]
        Calculates diurnal, semi-diurnal, and ter-diurnal harmonic components related to variations in local time.
    calculate_solar_zenith_angles() -> Tuple[float, float]
        Calculates solar zenith angles and corrections based on latitude and sun declination.
    calculate_local_time_at_beginning_of_bite_out() -> float
        Calculates the local time at the beginning of the bite-out phenomenon.
    calculate_summer_daytime_bite_out() -> float
        Models the summer daytime bite-out effect based on various parameters.
    calculate_local_time_F1() -> float
        Integrates the results from previous calculations to compute the local time variation factor F1.
    """

    def __init__(self, local_time_hours: int, latitude_radians: float, sun_declination_radians: float, day_of_year: int, coefficients: list):
        """
        Initializes a LocalTimeF1 instance with the given parameters.

        Parameters
        ----------
        local_time_hours : int
            The local time in hours for which variations are calculated.
        latitude_radians : float
            The geographic latitude in radians.
        sun_declination_radians : float
            The sun's declination angle in radians.
        day_of_year : int
            The day of the year for which calculations are performed.
        coefficients : list
            Coefficients used in the F1 calculation.
        """
        self.local_time_hours = local_time_hours
        self.latitude_radians = latitude_radians
        self.sun_declination_radians = sun_declination_radians
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    def calculate_local_time_variations(self) -> tuple[float, float, float]:
        """
        Calculates diurnal, semi-diurnal, and ter-diurnal harmonic components related to variations in local time.

        Returns
        -------
        variation_diurnal : float
            The diurnal harmonic component of local time variation.
        variation_semi_diurnal : float
            The semi-diurnal harmonic component of local time variation.
        variation_ter_diurnal : float
            The ter-diurnal harmonic component of local time variation.
        """
        phase_shift = 14

        variation_diurnal = (
            2 * math.pi * (self.local_time_hours - phase_shift)) / 24
        variation_semi_diurnal = (2 * math.pi * self.local_time_hours) / 12
        variation_ter_diurnal = (2 * math.pi * self.local_time_hours) / 8

        return variation_diurnal, variation_semi_diurnal, variation_ter_diurnal

    def calculate_solar_zenith_angles(self) -> tuple[float, float]:
        """
        Calculates solar zenith angles and corrections based on geographic latitude and sun declination.

        Returns
        -------
        cos_adjusted_zenith_angle : float
            The cosine of the adjusted solar zenith angle.
        cos_further_adjusted_zenith_angle : float
            The cosine of the further adjusted solar zenith angle.
        """
        solar_zenith_angle_correction = 0.4  # PF1

        cos_solar_zenith_angle = (math.sin(self.latitude_radians) * math.sin(self.sun_declination_radians)) + (
            math.cos(self.latitude_radians) * math.cos(self.sun_declination_radians))

        cos_adjusted_zenith_angle = math.cos(cos_solar_zenith_angle) - (
            ((2 * self.latitude_radians) / math.pi) * math.sin(self.sun_declination_radians))

        cos_further_adjusted_zenith_angle = math.cos(
            cos_solar_zenith_angle) + solar_zenith_angle_correction

        return cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle

    def calculate_local_time_at_beginning_of_bite_out(self):
        """
        Calculates the local time at the beginning of the bite-out phenomenon.

        Returns
        -------
        local_time_at_beginning_of_bite_out : float
            The local time at the beginning of the bite-out phenomenon.
        """
        local_time_at_beginning_of_bite_out = 13 + 1.5 * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * (
            self.latitude_radians / math.fabs(self.latitude_radians))

        return local_time_at_beginning_of_bite_out

    def calculate_summer_daytime_bite_out(self) -> float:
        """
        Models the summer daytime bite-out effect using several mathematical expressions involving latitude, day of the year, and other parameters.

        Returns
        -------
        summer_daytime_bite_out : float
            The modeled summer daytime bite-out effect.
        """
        local_time_at_beginning_of_bite_out = self.calculate_local_time_at_beginning_of_bite_out()
        fixed_geographic_latitude = 45
        gaussian_half_width_degree = 14
        gaussian_half_width_hours = 3

        summer_daytime_bite_out = math.exp(-(((math.fabs(self.latitude_radians) - fixed_geographic_latitude**2)) / (
            2 * gaussian_half_width_degree**2))) * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * math.exp(-((self.latitude_radians - local_time_at_beginning_of_bite_out)**2 / 2 * gaussian_half_width_hours**2)) * (self.latitude_radians / math.fabs(self.latitude_radians))

        return summer_daytime_bite_out

    def calculate_local_time_F1(self) -> float:
        """
        Integrates the results from previous calculations to compute the local time variation factor F1.

        Returns
        -------
        local_time_F1 : float
            The calculated local time variation factor F1.
        """
        variation_diurnal, variation_semi_diurnal, variation_ter_diurnal = self.calculate_local_time_variations()
        cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle = self.calculate_solar_zenith_angles()
        summer_daytime_bite_out = self.calculate_summer_daytime_bite_out()

        local_time_F1 = math.cos(cos_further_adjusted_zenith_angle) + (self.coefficients[0] * math.cos(variation_diurnal) + self.coefficients[1] * math.cos(variation_semi_diurnal) + self.coefficients[2] * math.sin(
            variation_semi_diurnal) + self.coefficients[3] * math.cos(variation_ter_diurnal) + self.coefficients[4] * math.sin(variation_ter_diurnal)) * math.cos(cos_adjusted_zenith_angle) + self.coefficients[5] * summer_daytime_bite_out

        return local_time_F1


class SeasonalVariationF2:
    """
    Calculates the seasonal variation of NmF2 (peak electron density) using the Neustrelitz Peak Density Model (NPDM).

    The seasonal variation is modeled by considering two components: the annual and semi-annual variations.
    Phase shifts of 18 days and 6 days are applied for the annual and semi-annual variations respectively, 
    with respect to the beginning of the year.

    ...

    Attributes
    ----------
    day_of_year : int
        The day of the year for which the seasonal variation is calculated.
    coefficients : list
        Coefficients used in the NPDM model for seasonal variation calculations.

    Methods
    ----------
    calculate_annual_variation()
        Calculates the annual variation component of NmF2.
    calculate_semi_annual_variation()
        Calculates the semi-annual variation component of NmF2.
    calculate_seasonal_variation_F2
        Calculates the total seasonal variation of NmF2
    """

    def __init__(self, day_of_year: int, coefficients: list):
        """
        Initializes the SeasonalVariationF2 instance with the day of the year and model coefficients.

        Parameters
        -------
        day_of_year : int
            The day of the year for which the seasonal variation is calculated.
        coefficients : list
            Coefficients used in the NPDM model for seasonal variation calculations.
        """
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    def calculate_annual_variation(self) -> float:
        """
        Calculates the annual variation component of NmF2.

        Returns
        -------
        annual_variation : float
            The calculated annual variation.
        """

        phase_shift = 18

        annual_variation = (
            2 * math.pi * (self.day_of_year - phase_shift)) / 365.25

        return annual_variation

    def calculate_semi_annual_variation(self) -> float:
        """
        Calculates the semi-annual variation component of NmF2.

        Returns
        -------
        semi_annual_variation : float
            The calculated semi-annual variation.
        """
        phase_shift = 6

        semi_annual_variation = (
            4 * math.pi * (self.day_of_year - phase_shift)) / 365.25

        return semi_annual_variation

    def calculate_seasonal_variation_F2(self) -> float:
        """
        Calculates the total seasonal variation of NmF2 by combining annual and semi-annual variations.

        Returns
        -------
        seasonal_variation_F2 : float
            The calculated seasonal variation of NmF2.
        """
        annual_variation = self.calculate_annual_variation()
        semi_annual_variation = self.calculate_semi_annual_variation()

        seasonal_variation_F2 = 1 + (self.coefficients[6] * math.cos(
            annual_variation)) + (self.coefficients[7] * math.cos(semi_annual_variation))

        return seasonal_variation_F2


class GeomagneticFieldDependencyF3:
    """
    Calculates the geomagnetic field dependency for the Neustrelitz Peak Density Model (NPDM).

    The geomagnetic field dependency is modeled as a function of geomagnetic latitude.

    ...

    Attributes
    ----------
    geommagnetic_latitude : float
        The geomagnetic latitude for which the dependency is calculated.
    coefficients : list 
        Coefficients used in the NPDM model for geomagnetic field dependency calculations.

    Methods
    ----------
    calculate_geomagentic_field_dependency()
        Calculates the geomagnetic field dependency
    """

    def __init__(self, geommagnetic_latitude: float, coefficients: list):
        """
        Initializes the GeomagneticFieldDependencyF3 instance.

        Parameters
        ----------
        geommagnetic_latitude : float
            The geomagnetic latitude for which the dependency is calculated.
        coefficients : list 
            Coefficients used in the NPDM model for geomagnetic field dependency calculations.
        """
        self.geommagnetic_latitude = geommagnetic_latitude
        self.coefficients = coefficients

    def calculate_geomagentic_field_dependency(self) -> float:
        """
        Calculates the geomagnetic field dependency based on the provided coefficients and geomagnetic latitude.

        Returns
        -------
        geomagentic_field_dependency_F3 : float
            The calculated geomagnetic field dependency.
        """
        geomagentic_field_dependency_F3 = 1 + \
            (self.coefficients[8] * math.cos(self.geommagnetic_latitude))

        return geomagentic_field_dependency_F3


class IonizationCrestsF4:
    """
    Calculates the ionization crest factors for the Neustrelitz Peak Density Model (NPDM).

    The ionization crest factors represent the ionization crests at specific geomagnetic latitudes and local times.

    ...

    Attributes
    ----------
    geommagnetic_latitude : float
        The geomagnetic latitude for which the ionization crest factors are calculated.
    local_time_hours : int 
        The local time (hours) for which the ionization crest factors are calculated.
    coefficients : list 
        Coefficients used in the NPDM model for ionization crest factor calculations.

    Methods
    ----------
    calculate_half_width()
        Calculates the half-width parameter for the ionization crest factor calculations.
    calculate_ionization_crest_1()
        Calculates the ionization crest factor for the northward crest at 16°N.
    calculate_ionization_crest_2()
        Calculates the ionization crest factor for the southward crest at -15°N.
    calculate_ionization_crest_F4()
        Calculates the overall ionization crest factor based on the provided coefficients, geomagnetic latitude, and local time.

    """

    def __init__(self, geommagnetic_latitude: float, local_time_hours: int, coefficients: list):
        """
        Initializes the IonizationCrestsF4 instance.

        Parameters
        ----------
        geommagnetic_latitude : float
            The geomagnetic latitude for which the ionization crest factors are calculated.
        local_time_hours : int 
            The local time (hours) for which the ionization crest factors are calculated.
        coefficients : list 
            Coefficients used in the NPDM model for ionization crest factor calculations.
        """

        self.geommagnetic_latitude = geommagnetic_latitude
        self.local_time_hours = local_time_hours
        self.coefficients = coefficients

    def calculate_half_width(self) -> float:
        """
        Calculates the half-width parameter for ionization crest factor calculations.

        Returns
        -------
        half_width : float
            The calculated half-width parameter.
        """

        coefficient_half_width_time = 12

        half_width = 20 - 10 * \
            math.exp(-((self.local_time_hours - 14)**2 /
                     (2 * coefficient_half_width_time**2)))

        return half_width

    def calculate_ionization_crest_1(self) -> float:
        """
        Calculates the ionization crest factor for the northward crest at 16°N.

        Returns
        -------
        ionization_crest_1 : float
            The calculated ionization crest factor for the northward crest.
        """

        half_width = self.calculate_half_width()
        northward_crest_degrees = 16

        ionization_crest_1 = - \
            ((self.geommagnetic_latitude - northward_crest_degrees) ** 2
             / (2 * half_width**2))

        return ionization_crest_1

    def calculate_ionization_crest_2(self) -> float:
        """
        Calculates the ionization crest factor for the southward crest at -15°N.

        Returns
        -------
        ionization_crest_2 : float
            The calculated ionization crest factor for the southward crest.
        """

        half_width = self.calculate_half_width()
        southward_crest_degrees = -15

        ionization_crest_2 = - \
            ((self.geommagnetic_latitude - southward_crest_degrees) ** 2
             / (2 * half_width**2))

        return ionization_crest_2

    def calculate_ionization_crest_F4(self) -> float:
        """
        Calculates the overall ionization crest factor based on the provided coefficients, geomagnetic latitude, and local time.

        Returns
        -------
        ionization_crest_F4 : float
            The calculated overall ionization crest factor.
        """

        ionization_crest_1 = self.calculate_ionization_crest_1()
        ionization_crest_2 = self.calculate_ionization_crest_2()

        ionization_crest_F4 = 1 + self.coefficients[9] * math.exp(
            ionization_crest_1) + self.coefficients[10] * math.exp(ionization_crest_2)

        return ionization_crest_F4


class SolarActivityF5:
    """
    Calculates the strong solar activity dependence for the Neustrelitz Peak Density Model (NPDM).

    The strong solar activity dependence is modeled as a function of solar radio flux F10.7.

    ...

    Attributes
    ----------
    solar_flux_F107 : float
        The solar radio flux F10.7 for which the solar activity dependence is calculated.
    coefficients : list 
        Coefficients used in the NPDM model for solar activity dependence calculations.

    Methods
    ----------
    calculate_solar_activity_F5()
        Calculates the solar activity dependence based on the provided coefficients and solar radio flux F10.7.

    """

    def __init__(self, solar_flux_F107: float, coefficients: list):
        """
        Initializes the SolarActivityF5 instance.

        Parameters
        ----------
        solar_flux_F107 : float
            The solar radio flux F10.7 for which the solar activity dependence is calculated.
        coefficients : list 
            Coefficients used in the NPDM model for solar activity dependence calculations.
        """
        self.solar_flux_F107 = solar_flux_F107
        self.coefficients = coefficients

    def calculate_solar_activity_F5(self) -> float:
        """
        Calculates the strong solar activity dependence based on the provided coefficients and solar radio flux F10.7 and delta F10.7.

        Returns
        -------
        solar_activity_F5 : float
            The calculated strong solar activity dependence.
        """
        delta_F107 = 12

        solar_activity_F5 = self.coefficients[11] + \
            self.coefficients[12] * self.solar_flux_F107 * delta_F107

        return solar_activity_F5


class NeustrelitzPeakDensityModel:
    """
    Calculates the peak electron density using the Neustrelitz Peak Density Model (NPDM).

    The NPDM combines various factors and coefficients to estimate the peak electron density (NmF2)
    in the ionosphere under different conditions.

    ...

    Attributes
    ----------
    local_time_F1 : float
        The local time variation factor (F1) calculated by the model.
    seasonal_variation_F2 : float
        The seasonal variation factor (F2) calculated by the model.
    geomagentic_field_dependency_F3 : float
        The geomagnetic field dependency factor (F3) calculated by the model.
    ionization_crest_F4 : float
        The ionization crest factor (F4) calculated by the model.
    solar_activity_F5 : float
        The strong solar activity dependence factor (F5) calculated by the model.

    Methods
    ----------
    calculate_neustrelitz_peak_electron_model()
        Calculates the peak electron density (NmF2) using the provided factors and coefficients.

    """

    def __init__(self, local_time_F1: float, seasonal_variation_F2: float, geomagentic_field_dependency_F3: float, ionization_crest_F4: float, solar_activity_F5: float):
        """
        Initializes the NeustrelitzPeakDensityModel instance with factors and coefficients.

        Parameters
        ----------
        local_time_F1 : float
            The local time variation factor (F1) calculated by the model.
        seasonal_variation_F2 : float
            The seasonal variation factor (F2) calculated by the model.
        geomagentic_field_dependency_F3 : float
            The geomagnetic field dependency factor (F3) calculated by the model.
        ionization_crest_F4 : float
            The ionization crest factor (F4) calculated by the model.
        solar_activity_F5 : float
            The strong solar activity dependence factor (F5) calculated by the model.
        """

        self.local_time_F1 = local_time_F1
        self.seasonal_variation_F2 = seasonal_variation_F2
        self.geomagentic_field_dependency_F3 = geomagentic_field_dependency_F3
        self.ionization_crest_F4 = ionization_crest_F4
        self.solar_activity_F5 = solar_activity_F5

    def calculate_neustrelitz_peak_electron_model(self) -> float:
        """
        Calculates the peak electron density (NmF2) using the provided factors and coefficients.

        Returns
        -------
        neustrelitz_peak_electron_model : float
            The calculated peak electron density (NmF2).
        """
        neustrelitz_peak_electron_model = self.local_time_F1 * self.seasonal_variation_F2 * \
            self.geomagentic_field_dependency_F3 * \
            self.ionization_crest_F4 * self.solar_activity_F5

        return neustrelitz_peak_electron_model


"""
TO-DOS:
- find out what units (degrees or radians) are used in the F4 class
- find out what the coefficients are
- find libraries & open API sources for the different variables
- create & implement intermediary conversion functions (ex. geographic latitude to geomagnetic latitude, etc.)
- plotting the results

"""

# Testing the classes

# time variables
local_time_hours = 18
day_of_year = 258
# location variables
latitude_radians = 0.867
geommagnetic_latitude = 0.049
# sun variables
sun_declination_radians = 0.8712
solar_flux_F107 = 1.5

coefficients = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

# Testing the LocalTimeF1 class & calculation
test_F1 = LocalTimeF1(local_time_hours, latitude_radians,
                      sun_declination_radians, day_of_year, coefficients)
results_F1 = test_F1.calculate_local_time_F1()
print(results_F1)

# Testing the SeasonalVariationF2 class & calculation
test_F2 = SeasonalVariationF2(day_of_year, coefficients)
results_F2 = test_F2.calculate_seasonal_variation_F2()
print(results_F2)

# Testing the GeomagneticFieldDependencyF3 class & calculation
test_F3 = GeomagneticFieldDependencyF3(geommagnetic_latitude, coefficients)
results_F3 = test_F3.calculate_geomagentic_field_dependency()
print(results_F3)

# Testing the IonizationCrestsF4 class & calculation
test_F4 = IonizationCrestsF4(
    geommagnetic_latitude, local_time_hours, coefficients)
result_F4 = test_F4.calculate_ionization_crest_F4()
print(result_F4)

# Testing the IonizationCrestsF4 class & calculation
test_F5 = SolarActivityF5(
    solar_flux_F107, coefficients)
result_F5 = test_F5.calculate_solar_activity_F5()
print(result_F5)


# Testing the NeustrelitzPeakElectronModel class & calculation
test_peak_electron_model = NeustrelitzPeakDensityModel(
    results_F1, results_F2, results_F3, result_F4, result_F5)
results_peak_electron_model = test_peak_electron_model.calculate_neustrelitz_peak_electron_model()
print(results_peak_electron_model)
