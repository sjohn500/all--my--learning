import React, { useContext } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { AuthContext } from '../context/AuthContext';

import LoginScreen from '../screens/LoginScreen';
import HomeScreen from '../screens/HomeScreen';
import AdminScreen from '../screens/AdminScreen';
import AnnouncementsScreen from '../screens/AnnouncementsScreen';
import CreateAnnouncementScreen from '../screens/CreateAnnouncementScreen';

const Stack = createStackNavigator();

const AppNavigator = () => {
  const { user } = useContext(AuthContext);

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {user ? (
          <>
            <Stack.Screen name="Home" component={HomeScreen} />
            <Stack.Screen name="Admin" component={AdminScreen} options={{ headerShown: true, title: 'Admin Dashboard' }} />
            <Stack.Screen name="Announcements" component={AnnouncementsScreen} options={{ headerShown: true, title: 'Announcements' }} />
            <Stack.Screen name="CreateAnnouncement" component={CreateAnnouncementScreen} options={{ headerShown: true, title: 'New Post' }} />
          </>
        ) : (
          <Stack.Screen name="Login" component={LoginScreen} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator;