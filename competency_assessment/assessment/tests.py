import unittest
from .models import Level, User, Competency, Strand, AssessmentPeriod, Rating, Assessment, AssessmentResults, Idp, Notifications, DirectManager

# Create your tests here.
class TestLevel(unittest.TestCase):
    """
    Class to test the behaviour of the Level class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)

    def tearDown(self):
        Level.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_level, Level))


class TestUser(unittest.TestCase):
    """
    Class to test behaviour of the User class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)

    def tearDown(self):
        User.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_user, User))


class TestCompetency(unittest.TestCase):
    """
    Class to test behaviour of the Competency class.
    """
    def setUp(self):
        self.new_competency = Competency('teamwork')

    def tearDown(self):
        Competency.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_competency, Competency))


class TestStrand(unittest.TestCase):
    """
    Class to test behaviour of the Strand class.
    """
    def setUp(self):
        self.new_competency = Competency('teamwork')
        self.new_strand = Strand('exemplary', self.new_competency)

    def tearDown(self):
        Strand.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_strand, Strand))

    
class TestAssessment_period(unittest.TestCase):
    """
    Class to test behaviour of the Assessment_period class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)
        self.new_assessment_period = AssessmentPeriod('2020/02/01', '2020/02/05', self.new_user)

    def tearDown(self):
        AssessmentPeriod.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_assessment_period, AssessmentPeriod))


class TestRating(unittest.TestCase):
    """
    Class to test behaviour of the Rating class.
    """
    def setUp(self):
        self.new_rating = Rating('top', 2)

    def tearDown(self):
        Rating.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_rating, Rating))


class TestAssessment(unittest.TestCase):
    """
    Class to test behaviour of Assessment class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)
        self.new_assessment_period = AssessmentPeriod('2020/02/01', '2020/02/05', self.new_user)
        self.new_assessment = Assessment(self.new_assessment_period, True, False)

    def tearDown(self):
        Assessment.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_assessment, Assessment))



class TestAssessment_results(unittest.TestCase):
    """
    Class to test the behaviour of Assessment_results class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)
        self.new_assessment_period = AssessmentPeriod('2020/02/01', '2020/02/05', self.new_user)
        self.new_assessment = Assessment(self.new_assessment_period, True, False)
        self.new_competency = Competency('teamwork')
        self.new_strand = Strand('exemplary', self.new_competency)
        self.new_rating = Rating('top', 2)
        self.new_assessment_results = AssessmentResults(self.new_assessment, 1, self.new_competency, self.new_strand, self.new_rating)

    def tearDown(self):
        AssessmentResults.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_assessment_results, AssessmentResults))


class TestIdp(unittest.TestCase):
    """
    Class to test the behaviour of Idp class.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)
        self.new_assessment_period = AssessmentPeriod('2020/02/01', '2020/02/05', self.new_user)
        self.new_assessment = Assessment(self.new_assessment_period, True, False)
        self.new_idp = Idp(self.new_assessment, 'This is an action', 'This is a resource', 'This is a target', 'This is a progress indicator', 'This is a nature of support')

    def tearDown(self):
        Idp.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_idp, Idp))



class TestNotifications(unittest.TestCase):
    def setUp(self):
        self.new_notification = Notifications('this is a sender', 'this is a receiver', 'This is an action', 'Seen!')

    def tearDown(self):
        Notifications.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_notification, Notifications))


class TestDirect_manager(unittest.TestCase):
    """
    Class that tests the behaviour of Direct_manager.
    """
    def setUp(self):
        self.new_level = Level('intermediate', 2)
        self.new_user = User('user@user.com', self.new_level)
        self.new_direct_manager = DirectManager(2, 'direct manager')

    def tearDown(self):
        DirectManager.objects.all().delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_direct_manager, DirectManager))