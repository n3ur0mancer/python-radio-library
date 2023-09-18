import math


class LocalTimeF1:
    def __init__(self, local_time_hours: int, latitude_radians: float, sun_declination_radians: float, day_of_year: int, coefficients: list):
        self.local_time_hours = local_time_hours
        self.latitude_radians = latitude_radians
        self.sun_declination_radians = sun_declination_radians
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    # method calculates diurnal, semi-diurnal, and ter-diurnal harmonic components related to variations in local time
    def calculate_local_time_variations(self) -> float:
        phase_shift = 14
        variation_diurnal = (
            2 * math.pi * (self.local_time_hours - phase_shift)) / 24
        variation_semi_diurnal = (2 * math.pi * self.local_time_hours) / 12
        variation_ter_diurnal = (2 * math.pi * self.local_time_hours) / 8
        return variation_diurnal, variation_semi_diurnal, variation_ter_diurnal

    # method calculates various angles related to solar zenith angles based on geographic latitude and sun declination
    def calculate_solar_zenith_angles(self) -> float:
        PF1 = 0.4
        cos_solar_zenith_angle = (math.sin(self.latitude_radians) * math.sin(self.sun_declination_radians))+(
            math.cos(self.latitude_radians) * math.cos(self.sun_declination_radians))
        cos_adjusted_zenith_angle = math.cos(cos_solar_zenith_angle) - (
            ((2 * self.latitude_radians) / math.pi) * math.sin(self.sun_declination_radians))
        cos_further_adjusted_zenith_angle = math.cos(
            cos_solar_zenith_angle) + PF1
        return cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle

    # method models the summer daytime bite-out effect using several mathematical expressions involving latitude, day of the year, and other parameters
    def calculate_summer_daytime_bite_out(self) -> float:
        LTBO = 13 + 1.5 * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * \
            (self.latitude_radians / math.fabs(self.latitude_radians))
        fixed_graographic_latitude = 45
        gaussian_half_width_degree = 14
        gaussian_half_width_hours = 3
        summer_daytime_bite_out = math.exp(-(((math.fabs(self.latitude_radians) - fixed_graographic_latitude**2)) / (
            2 * gaussian_half_width_degree**2))) * math.cos((2 * math.pi * (self.day_of_year - 181)) / 365.25) * math.exp(-((self.latitude_radians - LTBO)**2 / 2 * gaussian_half_width_hours**2)) * (self.latitude_radians / math.fabs(self.latitude_radians))
        return summer_daytime_bite_out

    # method integrates the results from the previous calculations to compute the local time variation factor F1
    def calculate_local_time_F1(self) -> float:
        variation_diurnal, variation_semi_diurnal, variation_ter_diurnal = self.calculate_local_time_variations()
        cos_adjusted_zenith_angle, cos_further_adjusted_zenith_angle = self.calculate_solar_zenith_angles()
        summer_daytime_bite_out = self.calculate_summer_daytime_bite_out()

        local_time_F1 = math.cos(cos_further_adjusted_zenith_angle) + (self.coefficients[0] * math.cos(variation_diurnal) + self.coefficients[1] * math.cos(variation_semi_diurnal) + self.coefficients[2] * math.sin(
            variation_semi_diurnal) + self.coefficients[3] * math.cos(variation_ter_diurnal) + self.coefficients[4] * math.sin(variation_ter_diurnal)) * math.cos(cos_adjusted_zenith_angle) + self.coefficients[5] * summer_daytime_bite_out
        return local_time_F1


class SeasonalVariationF2:
    def __init__(self, day_of_year: int, coefficients: list):
        self.day_of_year = day_of_year
        self.coefficients = coefficients

    # calculating the annual variation
    def calculate_annual_variation(self) -> float:
        phase_shift = 18
        annual_variation = (
            2 * math.pi * (self.day_of_year - phase_shift)) / 365.25
        return annual_variation

    # calculating the semi-annual variation
    def calculate_semi_annual_variation(self) -> float:
        phase_shift = 6
        semi_annual_variation = (
            4 * math.pi * (self.day_of_year - phase_shift)) / 365.25
        return semi_annual_variation

    # calculating the seasonal variation
    def calculate_seasonal_variation_F2(self) -> float:
        annual_variation = self.calculate_annual_variation()
        semi_annual_variation = self.calculate_semi_annual_variation()

        seasonal_variation_F2 = 1 + (self.coefficients[6] * math.cos(
            annual_variation)) + (self.coefficients[7] * math.cos(semi_annual_variation))
        return seasonal_variation_F2


class GeomagneticFieldDependencyF3:
    def __init__(self, geommagnetic_latitude: float, coefficients: list):
        self.geommagnetic_latitude = geommagnetic_latitude
        self.coefficients = coefficients

    def calculate_geomagentic_field_dependency(self) -> float:
        geomagentic_field_dependency_F3 = 1 + \
            (self.coefficients[8] * math.cos(geommagnetic_latitude))
        return geomagentic_field_dependency_F3


class IonizationCrestsF4:
    def __init__(self, geommagnetic_latitude: float, local_time_hours: int, coefficients: list):
        self.geommagnetic_latitude = geommagnetic_latitude
        self.local_time_hours = local_time_hours
        self.coefficients = coefficients

    def calculate_half_widths(self) -> float:
        coefficient_local_time = 12
        half_width = 20 - 10 * \
            math.exp(-((self.local_time_hours - 14) **
                     2 / (2 * coefficient_local_time**2)))
        return half_width

    def calculate_ionization_crest_1(self) -> float:
        half_width = self.calculate_half_widths()
        northward_crest_degrees = 16
        ionization_crest_1 = - \
            ((self.geommagnetic_latitude - northward_crest_degrees)
             ** 2 / (2 * half_width**2))
        return ionization_crest_1

    def calculate_ionization_crest_2(self) -> float:
        half_width = self.calculate_half_widths()
        southward_crest_degrees = -15
        ionization_crest_2 = - \
            ((self.geommagnetic_latitude - southward_crest_degrees)
             ** 2 / (2 * half_width**2))
        return ionization_crest_2

    def calculate_ionization_crest_F4(self) -> float:
        ionization_crest_1 = self.calculate_ionization_crest_1()
        ionization_crest_2 = self.calculate_ionization_crest_2()
        ionization_crest_F4 = 1 + self.coefficients[9] * math.exp(
            ionization_crest_1) + self.coefficients[10] * math.exp(ionization_crest_2)
        return ionization_crest_F4


class SolarActivityF5:
    def __init__(self, solar_flux_F107: float, coefficients: list):
        self.solar_flux_F107 = solar_flux_F107
        self.coefficients = coefficients

    def calculate_solar_activity_F5(self) -> float:
        solar_activity_F5 = self.coefficients[11] + \
            self.coefficients[12] * self.solar_flux_F107
        return solar_activity_F5


class NeustrelitzPeakDensityModel:
    def __init__(self, local_time_F1: float, seasonal_variation_F2: float, geomagentic_field_dependency_F3: float, ionization_crest_F4: float, solar_activity_F5: float):
        self.local_time_F1 = local_time_F1
        self.seasonal_variation_F2 = seasonal_variation_F2
        self.geomagentic_field_dependency_F3 = geomagentic_field_dependency_F3
        self.ionization_crest_F4 = ionization_crest_F4
        self.solar_activity_F5 = solar_activity_F5

    def calculate_neustrelitz_peak_electron_model(self) -> float:
        neustrelitz_peak_electron_model = self.local_time_F1 * self.seasonal_variation_F2 * \
            self.geomagentic_field_dependency_F3 * \
            self.ionization_crest_F4 * self.solar_activity_F5
        return neustrelitz_peak_electron_model


# Testing the classes

# defining the variables
local_time_hours = 18
latitude_radians = 0.867
geommagnetic_latitude = 0.049
sun_declination_radians = 0.8712
day_of_year = 258
coefficients = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
solar_flux_F107 = 1.5

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
