// Generated by gencpp from file subscriber/AddTwoIntsResponse.msg
// DO NOT EDIT!


#ifndef SUBSCRIBER_MESSAGE_ADDTWOINTSRESPONSE_H
#define SUBSCRIBER_MESSAGE_ADDTWOINTSRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace subscriber
{
template <class ContainerAllocator>
struct AddTwoIntsResponse_
{
  typedef AddTwoIntsResponse_<ContainerAllocator> Type;

  AddTwoIntsResponse_()
    : sum(0)  {
    }
  AddTwoIntsResponse_(const ContainerAllocator& _alloc)
    : sum(0)  {
    }



   typedef int64_t _sum_type;
  _sum_type sum;




  typedef boost::shared_ptr< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> const> ConstPtr;

}; // struct AddTwoIntsResponse_

typedef ::subscriber::AddTwoIntsResponse_<std::allocator<void> > AddTwoIntsResponse;

typedef boost::shared_ptr< ::subscriber::AddTwoIntsResponse > AddTwoIntsResponsePtr;
typedef boost::shared_ptr< ::subscriber::AddTwoIntsResponse const> AddTwoIntsResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::subscriber::AddTwoIntsResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace subscriber

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'subscriber': ['/home/odroid/ecen490/catkin_odroid_ws/src/subscriber/msg'], 'std_msgs': ['/opt/ros/indigo/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "b88405221c77b1878a3cbbfff53428d7";
  }

  static const char* value(const ::subscriber::AddTwoIntsResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xb88405221c77b187ULL;
  static const uint64_t static_value2 = 0x8a3cbbfff53428d7ULL;
};

template<class ContainerAllocator>
struct DataType< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "subscriber/AddTwoIntsResponse";
  }

  static const char* value(const ::subscriber::AddTwoIntsResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 sum\n\
\n\
";
  }

  static const char* value(const ::subscriber::AddTwoIntsResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.sum);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER;
  }; // struct AddTwoIntsResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::subscriber::AddTwoIntsResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::subscriber::AddTwoIntsResponse_<ContainerAllocator>& v)
  {
    s << indent << "sum: ";
    Printer<int64_t>::stream(s, indent + "  ", v.sum);
  }
};

} // namespace message_operations
} // namespace ros

#endif // SUBSCRIBER_MESSAGE_ADDTWOINTSRESPONSE_H