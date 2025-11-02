import React, { useState, useEffect } from 'react';
import { 
  StyleSheet, 
  View, 
  Text, 
  TouchableOpacity, 
  ActivityIndicator, 
  Modal,
  FlatList,
  Dimensions,
  Animated
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import axios from 'axios';

// Auto-detect backend URL
const getApiUrl = () => {
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL;
  }
  return 'http://127.0.0.1:8000';
};

const API_BASE_URL = getApiUrl();
const { width: SCREEN_WIDTH } = Dimensions.get('window');
const CARD_WIDTH = SCREEN_WIDTH * 0.85;
const CARD_MARGIN = (SCREEN_WIDTH - CARD_WIDTH) / 2;

export default function App() {
  const [contentType, setContentType] = useState('movie'); // 'movie' or 'tv'
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showSplash, setShowSplash] = useState(true);
  const [selectedItem, setSelectedItem] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);

  const fetchRecommendations = async (type = contentType) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/recommend?type=${type}`);
      // Create infinite loop by triplicating the array
      const recommendations = response.data.recommendations || [];
      setItems([...recommendations, ...recommendations, ...recommendations]);
    } catch (error) {
      console.error('Error fetching content:', error);
      alert(`Failed to load content. Make sure the backend is running on ${API_BASE_URL}`);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/refresh?type=${contentType}`);
      const recommendations = response.data.recommendations || [];
      setItems([...recommendations, ...recommendations, ...recommendations]);
    } catch (error) {
      console.error('Error refreshing:', error);
      alert('Failed to refresh content');
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = (type) => {
    if (type !== contentType) {
      setContentType(type);
      setLoading(true);
      fetchRecommendations(type);
    }
  };

  const openModal = (item) => {
    setSelectedItem(item);
    setModalVisible(true);
  };

  useEffect(() => {
    // Show splash for 2 seconds
    const splashTimer = setTimeout(() => {
      setShowSplash(false);
    }, 2000);

    // Fetch initial recommendations
    fetchRecommendations();

    return () => clearTimeout(splashTimer);
  }, []);

  if (showSplash) {
    return <SplashScreen />;
  }

  if (loading && items.length === 0) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#4CAF50" />
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar style="auto" />
      
      {/* Toggle Tabs */}
      <View style={styles.toggleContainer}>
        <TouchableOpacity
          style={[styles.toggleButton, contentType === 'movie' && styles.toggleButtonActive]}
          onPress={() => handleToggle('movie')}
        >
          <Text style={[styles.toggleText, contentType === 'movie' && styles.toggleTextActive]}>
            Movies
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.toggleButton, contentType === 'tv' && styles.toggleButtonActive]}
          onPress={() => handleToggle('tv')}
        >
          <Text style={[styles.toggleText, contentType === 'tv' && styles.toggleTextActive]}>
            TV Shows
          </Text>
        </TouchableOpacity>
      </View>

      {/* Carousel */}
      <FlatList
        data={items}
        horizontal
        pagingEnabled={false}
        showsHorizontalScrollIndicator={false}
        snapToInterval={CARD_WIDTH + 16}
        decelerationRate="fast"
        contentContainerStyle={styles.carouselContent}
        keyExtractor={(item, index) => `${item.id}-${index}`}
        renderItem={({ item, index }) => (
          <CarouselCard
            item={item}
            onPress={() => openModal(item)}
            index={index}
          />
        )}
        getItemLayout={(data, index) => ({
          length: CARD_WIDTH + 16,
          offset: (CARD_WIDTH + 16) * index,
          index,
        })}
        initialScrollIndex={items.length > 0 ? Math.floor(items.length / 3) : 0}
        onScrollToIndexFailed={() => {}}
      />

      {/* Refresh Button */}
      <TouchableOpacity
        style={styles.refreshButton}
        onPress={handleRefresh}
        disabled={loading}
      >
        {loading ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text style={styles.refreshButtonText}>↻ Refresh</Text>
        )}
      </TouchableOpacity>

      {/* Detail Modal */}
      <DetailModal
        visible={modalVisible}
        item={selectedItem}
        onClose={() => setModalVisible(false)}
      />
    </View>
  );
}

function SplashScreen() {
  return (
    <View style={styles.splashContainer}>
      <Text style={styles.splashLogo}>CineDeen</Text>
      <Text style={styles.splashSubtitle}>Islamic Media Recommender</Text>
      <ActivityIndicator size="large" color="#fff" style={{ marginTop: 20 }} />
    </View>
  );
}

function CarouselCard({ item, onPress }) {
  return (
    <TouchableOpacity
      style={styles.carouselCard}
      onPress={onPress}
      activeOpacity={0.9}
    >
      <View style={styles.cardHeader}>
        <Text style={styles.cardTitle} numberOfLines={2}>{item.title}</Text>
        <View style={styles.ratingBadge}>
          <Text style={styles.ratingText}>⭐ {item.vote_average}</Text>
        </View>
      </View>
      
      <Text style={styles.releaseDate}>{item.release_date}</Text>
      
      <Text style={styles.cardSummary} numberOfLines={4}>
        {item.islamic_summary}
      </Text>
      
      <View style={styles.tapHint}>
        <Text style={styles.tapHintText}>Tap to see more</Text>
      </View>
    </TouchableOpacity>
  );
}

function DetailModal({ visible, item, onClose }) {
  if (!item) return null;

  return (
    <Modal
      animationType="slide"
      transparent={true}
      visible={visible}
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <TouchableOpacity style={styles.closeButton} onPress={onClose}>
            <Text style={styles.closeButtonText}>✕</Text>
          </TouchableOpacity>

          <Text style={styles.modalTitle}>{item.title}</Text>
          
          <View style={styles.modalRating}>
            <Text style={styles.modalRatingText}>⭐ {item.vote_average}</Text>
            <Text style={styles.modalDate}>{item.release_date}</Text>
          </View>

          <View style={styles.divider} />

          <Text style={styles.sectionTitle}>Islamic Perspective</Text>
          <Text style={styles.modalSummary}>{item.islamic_summary}</Text>

          {item.themes && item.themes.length > 0 && (
            <>
              <Text style={styles.sectionTitle}>Themes</Text>
              <View style={styles.themesContainer}>
                {item.themes.map((theme, idx) => (
                  <View key={idx} style={styles.themeTag}>
                    <Text style={styles.themeText}>{theme}</Text>
                  </View>
                ))}
              </View>
            </>
          )}
        </View>
      </View>
    </Modal>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    paddingTop: 50,
  },
  toggleContainer: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    marginHorizontal: 20,
    marginVertical: 16,
    borderRadius: 25,
    padding: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  toggleButton: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderRadius: 20,
  },
  toggleButtonActive: {
    backgroundColor: '#4CAF50',
  },
  toggleText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  toggleTextActive: {
    color: '#fff',
  },
  carouselContent: {
    paddingHorizontal: 8,
  },
  carouselCard: {
    width: CARD_WIDTH,
    backgroundColor: '#fff',
    borderRadius: 16,
    padding: 20,
    marginHorizontal: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 5,
    minHeight: 280,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  cardTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    marginRight: 10,
  },
  ratingBadge: {
    backgroundColor: '#FFC107',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 16,
  },
  ratingText: {
    color: '#333',
    fontWeight: '600',
    fontSize: 14,
  },
  releaseDate: {
    fontSize: 13,
    color: '#888',
    marginBottom: 16,
  },
  cardSummary: {
    fontSize: 15,
    color: '#555',
    lineHeight: 22,
    flex: 1,
  },
  tapHint: {
    alignItems: 'center',
    marginTop: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#e0e0e0',
  },
  tapHintText: {
    fontSize: 13,
    color: '#4CAF50',
    fontWeight: '600',
  },
  refreshButton: {
    backgroundColor: '#4CAF50',
    padding: 16,
    alignItems: 'center',
    justifyContent: 'center',
    margin: 20,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 4,
    elevation: 4,
  },
  refreshButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#666',
  },
  // Modal Styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.6)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 24,
    width: '90%',
    maxHeight: '80%',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 10,
  },
  closeButton: {
    position: 'absolute',
    top: 16,
    right: 16,
    zIndex: 1,
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: '#f0f0f0',
    alignItems: 'center',
    justifyContent: 'center',
  },
  closeButtonText: {
    fontSize: 20,
    color: '#666',
    fontWeight: 'bold',
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 12,
    marginRight: 40,
  },
  modalRating: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  modalRatingText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFC107',
    marginRight: 12,
  },
  modalDate: {
    fontSize: 14,
    color: '#888',
  },
  divider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginVertical: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: '#4CAF50',
    marginBottom: 12,
    marginTop: 8,
  },
  modalSummary: {
    fontSize: 15,
    color: '#555',
    lineHeight: 24,
    marginBottom: 16,
  },
  themesContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 12,
  },
  themeTag: {
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 18,
    marginRight: 8,
    marginBottom: 8,
  },
  themeText: {
    fontSize: 13,
    color: '#2E7D32',
    fontWeight: '600',
  },
  // Splash Screen
  splashContainer: {
    flex: 1,
    backgroundColor: '#4CAF50',
    justifyContent: 'center',
    alignItems: 'center',
  },
  splashLogo: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  splashSubtitle: {
    fontSize: 16,
    color: '#fff',
    opacity: 0.9,
  },
});
